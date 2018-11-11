import data_process as dp
import feature_extract as fe
import model as model

def main(file):
    x = dp.process_string(file)
    ft = fe.get_tag_info(x)
    pr = model.train(ft)[0] 
    if pr == 1:
        return true:
    return false; 