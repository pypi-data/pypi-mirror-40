import tensorflow as tf
import numpy as np
from . import predutil
from aquests.lib.termcolor import tc
from sklearn.utils.extmath import softmax
        
class Result:
    train_dir = None
    labels = None
    name = None
    _perfmetric_func = None
    _summary_func = None        
            
    def __init__ (self, xs, ys, logits, cost, performance, ops, args, epoch, global_step, is_validating, on_ftest):
        self.xs = xs
        self.ys = ys
        self.logits = logits
        self.cost = cost        
        self.performance = performance
        self.epoch = epoch
        self.global_step = global_step
        self.is_validating = is_validating
        self.ops = ops
        self.args = args
        
        # set by trainer
        self.is_cherry = False
        self.on_ftest = on_ftest
        self.is_overfit = False
        self.is_improved = False
        if performance is not None and self._perfmetric_func: # no run within batch steps
            self.performance = self._perfmetric_func (self)
            
    @property
    def x (self):
        return self.xs
    
    @property
    def y (self):
        return self.ys
    
    @property
    def logit (self):
        return self.logits
    
    @property
    def phase (self):
        if self.on_ftest:
            return "final"
        elif self.is_cherry:
            return "saved"            
        return self.is_validating  and 'resub' or 'valid'
        
    def __make_summary (self, d = {}):
        d  ["eval/cost"] = self.cost
        if isinstance (self.performance, (tuple, list)):
            vals = []
            for i in range (len (self.performance)):
                try: 
                    name, val = self.performance [i]
                except TypeError:
                    try:
                        name = self.labels [i].name
                        val = self.performance [i]
                    except (IndexError, TypeError):
                        name, val = str (i + 1), self.performance [i]                                                
                name = "eval/acc/" + name                        
                d [name] = val
                vals.append (val)
            d ["eval/acc/avg"] = np.mean (vals)
            
        elif self.performance:
            try:
                name, val = self.performance
                d ["eval/acc"] = val
            except TypeError:
                d ["eval/acc"] = self.performance
        
        d_ = {}
        for k, v in d.items ():
            if self.name:
                k = "{}:{}".format (self.name, k)
            if isinstance (v, (list, tuple)):
                if len (v) == 1: v = v [0]
                else: raise ValueError ("Required float, int or an array contains only one of them")
            d_ [k] = v        
        return d_
    
    def __get_phase_summary (self, kargs):
        output = []
        for k, v in self.__make_summary (kargs).items ():                            
            if isinstance (v, (float, np.float64, np.float32)):
                output.append ("{} {:.5f}".format (k, v))
            elif isinstance (v, (int, np.int64, np.int32)):
                output.append ("{} {:04d}".format (k, v))
            else:
                raise ValueError ("Required float, int type")
        output.sort ()
        
        if self.on_ftest:
            return " | ".join (output)            
        if self.phase != "saved":
            if self.is_overfit:
                output.append (tc.error ("overfitted"))
            if self.is_improved:
                output.append (tc.info ("improved"))
        return " | ".join (output)
    
    def summary (self):
        self._summary_func (self.phase, self.__make_summary (self.args.get ("summary", {})))
        return self
    
    # statistics helper methods -----------------------------------------    
    def log (self, msg = None, **kargs):
        coloring = False
        if not msg:
            msg = self.__get_phase_summary (kargs)
            coloring = True
        phase = self.phase
        if phase == "final":
            header = "[fin.:ftest]"
            color = tc.fail              
        else:    
            header = "[{:04d}:{}]".format (self.epoch, self.phase)                                  
            color = phase == "saved" and tc.warn or tc.debug                   
        print ("{} {}".format ((coloring and color or tc.critical) (header), msg))
        return self

    def reunion (self, data_length, unify_func = np.mean, softmaxing = True):
        logits = []
        ys = []
        index = 0
        for part_length in data_length:        
            ys.append (self.ys [index])
            aud = self.logits [index: index + part_length]
            if softmaxing:
                aud = softmax (aud)                
            index += part_length
            logits.append (unify_func (aud, 0))
        self.logits = np.array (logits)
        self.ys = np.array (ys)
    
    def get_confusion_matrix (self, logits = None, ys = None):
        if logits is None:
            logits = self.logits
        if ys is None:
            ys = self.ys
        mat_ = predutil.confusion_matrix (
            np.argmax (logits, 1), 
            np.argmax (ys, 1),
            logits.shape [1]
        )
        return mat_.T
    
    def slice_by_label (self, label_index):
        start_index = 0
        for i in range (label_index + 1):
            num_label = len (self.labels [i])
            if label_index == i:
                break
            start_index += num_label        
        logits = self.logits [:, start_index:start_index + num_label]
        ys = self.ys [:, start_index:start_index + num_label]
        return logits, ys
    
    @property    
    def metric (self):
        class Metric:
            def __init__ (self):
                class Tri:
                    def __init__ (self):
                        self.micro = []
                        self.macro = []
                        self.weighted = []                        
                self.accuracy = []
                self.precision = Tri ()
                self.recall = Tri ()
                self.f1 = Tri ()
            
        metric = Metric ()
        if self.labels is None:
            self.calculate_metric (metric, self.logits, self.ys)
        else:            
            for idx, label in enumerate (self.labels):
                logits, ys = self.slice_by_label (idx)
                self.calculate_metric (metric, logits, ys)
        return metric
    
    def calculate_metric (self, metric, logits, ys):
        mat = self.get_confusion_matrix (logits, ys)
        catpreds = mat.sum (axis = 0)
        table = np.zeros ([mat.shape [0], 3])
        for idx, preds in enumerate (mat.T):
            tp = preds [idx]
            fp = catpreds [idx] - tp            
            table [idx][0] = tp
            table [idx][1] = fp
            
        catans = mat.sum (axis = 1)
        for idx, ans in enumerate (mat):
            tp = ans [idx]
            fn = catans [idx] - tp
            table [idx][2] = fn                
        
        accuracy = np.sum (table [:, 0]) / len (logits)
        micro_precision = np.sum (table [:, :1]) / np.sum (table [:, :2])
        micro_recall = np.sum (table [:, :1]) / np.sum ([table [:, 0], table [:, 2]])
        metric.accuracy.append (accuracy)                        
        metric.precision.micro.append (micro_precision)
        metric.recall.micro.append (micro_recall)
        metric.f1.micro.append (2 / (1 / micro_precision + 1 / micro_recall))
        
        macro_precisions = []
        macro_recalls = []            
        weighted_precisions = []
        weighted_recalls = []
        
        for cat, (tp, fp, fn) in enumerate (table):
            weight = catans [cat] / np.sum (catans)
            if tp + fp == 0:
                macro_precisions.append (0.0)
            else:
                macro_precisions.append (tp / (tp + fp))
                weighted_precisions.append (tp / (tp + fp) * weight)
                
            if tp + fn == 0:
                macro_recalls.append (0.0)
            else:
                macro_recalls.append (tp / (tp + fn))
                weighted_recalls.append (tp / (tp + fn) * weight)
                
        macro_precision = np.mean (macro_precisions)
        macro_recall = np.mean (macro_recalls)
        weighted_precision = np.sum (weighted_precisions)
        weighted_recall = np.sum (weighted_recalls)
        
        metric.precision.macro.append (macro_precision)
        metric.recall.macro.append (macro_recall)            
        metric.f1.macro.append (2 / (1 / macro_precision + 1 / macro_recall))
                    
        metric.precision.weighted.append (weighted_precision)
        metric.recall.weighted.append (weighted_recall)            
        metric.f1.weighted.append ((2 / (1 / weighted_precision + 1 / weighted_recall)))  
            
    def confusion_matrix (self, num_label = 0, label_index = 0, indent = 13, show_label = True):
        start_index = 0
        if num_label == 0:
            if not self.labels:
                raise ValueError ("num_label required")            
            logits, ys = self.slice_by_label (label_index)
        else:
            logits = self.logits [:, :num_label]
            ys = self.ys [:, :num_label]
            
        mat_ = self.get_confusion_matrix (logits, ys)        
        mat = str (mat_) [1:-1]
        self.log ("confusion matrix")
        
        labels = []
        if show_label and self.labels:
            cur_label = self.labels [label_index]
            first_row_length = len (mat.split ("\n", 1) [0]) - 2
            label_width = (first_row_length - 1) // mat_.shape [-1]
            labels = [str (each) [:label_width].rjust (label_width) for each in cur_label.items ()]            
            print (tc.fail ((" " * (indent + label_width + 1)) + " ".join (labels)))
            
        lines = []
        for idx, line in enumerate (mat.split ("\n")):
            if idx > 0:
                line = line [1:]
            line = line [1:-1]                    
            if labels:    
                line = tc.info (labels [idx]) + " " + line
            if indent:    
                line = (" " * indent) + line
            print (line)

    def logit_range (self):
        output_range = [self.logit.min (), self.logit.max (), np.mean (self.logit), np.std (self.logit)]
        quant_range = {}
        for idx, m in enumerate (self.logit [:,:29].argsort (1)[:,-2]):
            sec = int (self.logit [idx, m])
            try: quant_range [sec] += 1
            except KeyError: quant_range [sec] = 1
        quant_range = quant_range
        if quant_range:           
            stats = sorted (quant_range.items ())
            # output range for top1: {} ~ {}, logit range: {:.3f} ~ {:.3f}, mean: {:.3f} std: {:.3f}
            return stats [0][0] - 1, stats [-1][0] + 1, output_range [0], output_range [1], output_range [2], output_range [3]                                
        
    def confidence_level (self, label_index = 0):
        label = self.labels [label_index]
        stat = {}
        for idx in range (len (self.y)):
            logit = self.logit [idx][:len (label)]
            y = self.y [idx][:len (label)]
            probs = predutil.softmax (logit)
            prob = "{:.5f}".format (probs [np.argmax (probs)])
            if prob not in stat:
                stat [prob] = [0, 0]
            if np.argmax (probs) == np.argmax (y):    
                stat [prob][0] += 1
            stat [prob][1] += 1
            
        ordered = [] 
        accum = 0        
        accum_t = 0
        total = len (self.y)
        for lev, (c, t) in sorted (stat.items (), reverse = True):            
            accum += c            
            accum_t += t
            accuracy = accum / accum_t * 100
            ordered.append ((
                lev, 
                accum, accum_t, accuracy, 
                accum / total * 100 
            ))
            if len (ordered) >= 10 and accuracy < 100.:
                break
        return ordered    
    
