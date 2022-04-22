import json
import sys
import shutil
import re
import pyperclip
import time
from pathlib import Path
from functools import reduce
from PIL import Image, ImageChops
from flask import Flask, request

app = Flask(__name__)
@app.route('/frame/<id>')
def frame(id):
    if "static" in request.args:
        print(request.args)
if __name__ == "__main__":
    app.run()