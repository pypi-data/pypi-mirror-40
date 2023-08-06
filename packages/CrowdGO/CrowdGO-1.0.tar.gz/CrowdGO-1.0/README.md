pip3 install sklearn
pip3 install pandas
pip3 install numpy

python3 CrowdGO.py -i example_input/input.tab -r example_output_training/randomForest.pkl -o example_output

python3 CrowdGO_training.py -i example_input/training.tab -o example_output_training
