import data_process as dp
import feature_extract as fe
import model as model

def main(file):
    x = dp.process_string(file)
    ft = fe.get_tag_info(x)
    pr = model.train(ft)[0] 
    if (pr > .50):
        return "We're noticing something about your voice. Please consider seeing a doctor."
    else:
        return "You are sounding very healthy! Have a great day!"