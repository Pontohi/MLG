cd ..
python train.py --tdirs DailyGarf --shape 128 128 3 --batch 48 --epochs 500000 --imgrate 500 --modelrate 2500 --label DailyGarf
echo "Finished Training"