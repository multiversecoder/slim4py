from slim4py.slim import Slim

if __name__ == '__main__':

    slim = Slim("slim")

    print(slim.render("example_slim.slim", year="2019", author="https://github.com/multiversecoder/slim4py"))
