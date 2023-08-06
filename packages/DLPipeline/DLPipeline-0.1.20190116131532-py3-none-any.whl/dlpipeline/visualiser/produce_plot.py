from tkinter.filedialog import Tk, askopenfilename
from tkinter.simpledialog import askstring

import pandas as pd
from matplotlib import pyplot as plt


def main():
  Tk().withdraw()
  filename = askopenfilename()
  training_data = pd.read_csv(filename)

  Tk().withdraw()
  filename = askopenfilename()
  validation_data = pd.read_csv(filename)

  train, *_ = plt.plot(training_data.Step, training_data.Value, label='Traning')
  val, *_ = plt.plot(validation_data.Step, validation_data.Value, label='Validation')

  plt.legend(handles=[train, val])
  name = askstring('Plot name', 'Plot name')
  plt.title(f'{name}: Training + Validation')
  y_name = askstring('Y name', 'Y Name')
  plt.ylabel(y_name)
  plt.xlabel('Epochs')

  plt.show()


if __name__ == '__main__':
  main()
