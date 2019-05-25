cd ..
python train.py --tdirs Strips --shape 304 96 3 --batch 12 --epochs 500000 --imgrate 500 --modelrate 2500 --label GarfStrips
echo "Finished Training"