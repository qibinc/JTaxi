# JTaxi

Tsinghua Database Final Project.

## Dependencies

- [metis](http://glaros.dtc.umn.edu/gkhome/metis/metis/overview)
- Python3.6, numpy

## Preprocessing

```bash
cd src
make    # compile core.cpp
./core load
```

- This will generate 2 `.data` files under directory data.

## Run

```bash
cd src
python search.py
# Input
# Example: Tsinghua to Summer Palace
116.34189 40.014997 116.287223 40.00341
# Then open index.html
```

- Note: first query may take a while since the `.data` files are being loaded. Later queries will be within 5 seconds.

## Result

![Result](http://otukr87eg.bkt.clouddn.com/0f6029aa43872934c58a3daabe8ff62d.jpg)
