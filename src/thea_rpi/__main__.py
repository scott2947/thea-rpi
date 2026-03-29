from thea_rpi.split_pipeline import SplitPipeline
from thea_rpi.action.head.actor import HeadActor


if __name__ == "__main__":
    spl = SplitPipeline("head", HeadActor())
    spl.start()
    spl.run()
