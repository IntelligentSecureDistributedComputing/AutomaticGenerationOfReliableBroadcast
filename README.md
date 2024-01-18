# Generating Fault-Tolerant Reliable Broadcast Algorithms using Reinforcement Learning

This repository presents an approach to generating fault-tolerant reliable broadcast algorithms using Reinforcement Learning. The default behavior is to generate non-fault-tolerant algorithms. However, this can be configured to generate fault-tolerant algorithms for different failure modes (see [Configuration](#configuration) section).
# Getting Started (Locally)

These instructions will get you a copy of the project up and running on your local machine.

## Pre-requisites
 * Python 3.10 virtual environment installed. To do that, you can run:
    ```bash
    sudo apt install python3.10-venv
    ```
 * Ports 5001, 5002 and 5003 available.

## 1. Setup & Run Generator

1. Go to folder ```Generator``` and open a terminal.

2. On the folder  ```Generator``` run:
    ```bash
    ./scripts/local/setup.sh
    ```
    This will create the .env file and install the python libraries.

3. On the folder  ```Generator``` run:
    ```bash
    ./scripts/local/start.sh
    ```
    This will start the Generator component. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Generator_shell.png?raw=true)
    
## 2. Setup & Run Validator

1. Go to folder ```Validator``` and open a terminal.

2. On the folder  ```Validator``` run:
    ```bash
    ./scripts/local/setup.sh
    ```
    This will create the .env file, install the python libraries and the spin framework.

3. On the folder  ```Validator``` run:
    ```bash
    ./scripts/local/start.sh
    ```
    This will start the Validator component. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Validator_shell.png?raw=true)

## 3. Start generating the algorithm
1. Go to folder ```Client``` and open a terminal.

2. On the folder  ```Client``` run:
    ```bash
    ./scripts/local/setup.sh
    ```
    This will create the .env file and install the python libraries.

3. On the folder  ```Client``` run:
    ```bash
    ./scripts/local/start_RBLearner.sh
    ```
    This will start the process of generating the Reliable Broadcast algorithm on the foreground. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Client_shell.png?raw=true) 
    
    You will be able to follow both generation and validation processes on the ```Generator``` and ```Validator``` terminals, respectively. A folder with the name ```output``` will appear on the root of the folder ```Generator``` from where the simulator will output the progress of the generation process.

# Getting Started (Docker)

These instructions will get you a copy of the project up and running on your local machine using Docker.
## Pre-requisites
 * Docker and Docker-compose installed (https://docs.docker.com/compose/install/).

## 1. Setup & Run Generator

1. Go to folder ```Generator``` and open a terminal.

2. On the folder  ```Generator``` run:
    ```bash
    ./scripts/docker/setup.sh
    ```
    This will create the Generator docker image.

3. On the folder  ```Generator``` run:
    ```bash
    ./scripts/docker/start.sh
    ```
    This will start the Generator container. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Generator_docker_shell.png?raw=true) 

## 3. Setup & Run Validator

1. Go to folder ```Validator``` and open a terminal.

2. On the folder  ```Validator``` run:
    ```bash
    ./scripts/docker/setup.sh
    ```
    This will create the Validator docker image.

3. On the folder  ```Validator``` run:
    ```bash
    ./scripts/docker/start.sh
    ```
    This will start the Validator container. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Validator_docker_shell.png?raw=true) 

## 3. Start generating the algorithm

1. Go to folder ```Client``` and open a terminal.

2. On the folder  ```Client``` run:
    ```bash
    ./scripts/docker/setup.sh
    ```
    This will create the Client docker image.

3. On the folder  ```Client``` run:
    ```bash
    ./scripts/docker/start_RBLearner.sh
    ```
    This will start the process of generating the Reliable Broadcast algorithm on the foreground. In the end, this is what you should see:
    
    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Client_docker_shell.png?raw=true) 
    
    You will be able to follow both generation and validation processes on the ```Generator``` and ```Validator``` terminals, respectively. A folder with the name ```output``` will appear on the root of the folder ```Generator``` from where the simulator will output the progress of the generation process. This folder will appear both locally and on the docker container.

# Configuration

The inputs can be changed in order to study different problems and find innovative solutions. In this section, I show you how to update some parameters of the inputs.

**Note: these are only two possible examples of configuration. If you need help and want to change other inputs, please contact me.**
## Failure Mode

The default failure-mode is the **No-Failure** mode. To change this input to generate a **Crash-Failure** or **Byzantine-Failure** algorithms:

1. Go to the folder ```Client/inputs/Validation``` and open the file ```validation_inputs.jsonc```.

2. There you will see a ```FailureMode``` property containing 3 objects: ```NO_FAILURE```, ```CRASH_FAILURE``` and ```BYZANTINE_FAILURE```.

    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Failure_mode_property.png?raw=true)

3. Each ```FailureMode``` contains a ```Mode``` property with a boolean value. Change the ```Mode``` property to ```true```  **only** on the failure mode that you want to test. 

**Note:** only one failure mode will be tested even if you put ``true``in all cases. The order is **No-Failure -> Crash-Failure -> Byzantine-Failure**.

## Number of Episodes

When changing the properties of the algorithm to be generated, an higher number of episodes may be needed to train the agent. To change that:

1. Go to the folder ```Client/inputs/Generation``` and open the file ```generation_inputs.jsonc```.

2. There you will see a ```NumberOfEpisodes``` property (default value is 1000) that you can change to a higher value.

    ![alt text](https://github.com/diogolvaz/FAULTAGE/blob/Reliable-Broadcast/misc/Number_of_episodes.png?raw=true)


# Implementation

Different technologies were used to implement this approach. Here we present the main technologies used. 

**Note: this code is for research purposes, meaning that programming issues are of secondary importance.**

### Built With
* [Python](https://www.python.org/) - development of both Validator e Generator components 
* [Spin](https://spinroot.com/spin/whatispin.html) - framework used to validate the algorithms 
* [Promela](https://en.wikipedia.org/wiki/Promela) - language used to write the validation models to be executed by Spin

