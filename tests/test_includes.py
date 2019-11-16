from slim4py.slim import Slim

if __name__ == '__main__':

    slim = Slim("slim")

    greet="Hi Bro"

    print(slim.render("example_includes.slim", greet=greet, year="2019", author="https://github.com/multiversecoder/slim4py"))
