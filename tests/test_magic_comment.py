from slim4py.slim import Slim

if __name__ == '__main__':

    slim = Slim("slim")

    print(slim.render("example_magic_comment.slim", say_hello="Hello World", year="2019", author="https://github.com/multiversecoder/slim4py"))
