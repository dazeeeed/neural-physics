# Implementation of the artificial neural network in determining selected parameters of a nuclear reactor core

## Abstract
The aim of the research was to design and implement an Artificial Intelligence (AI) algorithm, namely an Artificial Neural Network (ANN) that can predict selected 
nuclear reactor core parameters for a given core loading pattern without running a core simulator. 
The reactor core model based on MIT PWR benchmark was used as a typical power reactor. The PARCS v3.2 core simulator was used as a full-core reactor physics solver 
to generate validation and test data for the ANN. The work is based to a large extent on the process of appropriate transformation of data generated by PARCS simulator, 
which was later used in the process of learning an artificial neural network with dedicated TensorFlow 2.0 implementation. Various methods that allow to obtain better 
accuracy of the predicted results were studied. Different network architectures were studied to find the optimal number of neurons in the hidden layers of the network 
which results were later compared with the architectures proposed in the literature. For the selected best architecture, predictions were made for different core 
parameters and their dependence on core loading patterns. For instance, the length of a single fuel cycle depending on the initial core loading pattern was predicted 
with good accuracy (>99\%). This work contributes to the exploration of the usefulness of neural networks in solving nuclear reactor physics problems, and in the future 
can be used to support the design of reactor cores.  

![Core configurations](https://github.com/dazeeeed/neural-physics/blob/main/data/graphics/generated_cores.png)

## Technologies 
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=TensorFlow&logoColor=white" /> <img src="https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white" /> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" />


## Sample predictions
![Reactivity vs days](https://github.com/dazeeeed/neural-physics/blob/main/data/graphics/reactivity_vs_days.png)

![Cycle length](https://github.com/dazeeeed/neural-physics/blob/main/data/graphics/cycle_length.png)


## License
Code in this repository is under [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) license.
