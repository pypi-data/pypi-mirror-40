from titanicsp.utils import Loader

class Prediction(object):
    def __init__(self, path):
        pass

    def predic(self, **kwargs):
        raise NotImplementedError()

class TitanicPrediction(Prediction):
    def __init__(self, path):
        super(TitanicPrediction, self).__init__(path)

    def predic(self, **kwargs):
        print(kwargs['age'])
        if kwargs['sex'] == 'male':
            sex=0
        elif kwargs['sex'] == 'female':
            sex=1
        else:
            raise NameError("Use male or female")

if __name__ == '__main__':
    tp = TitanicPrediction('file.pth')
    tp.predic(age=25, sex='male', cabin=1)

