set -ex

model="gas"
dataroot="./datasets/font"
name="gas_test_100ep_aug"
dataset_mode="font"

python3 test.py --dataroot ${dataroot}  --model ${model} --dataset_mode ${dataset_mode} --name ${name} --phase test_unknown_style  --eval --no_dropout
#python3 test.py --dataroot ${dataroot}  --model ${model} --dataset_mode ${dataset_mode} --name ${name} --phase test_unknown_content  --eval --no_dropout