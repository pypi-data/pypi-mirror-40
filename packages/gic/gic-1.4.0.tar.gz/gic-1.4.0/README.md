# GIC 

## An image compressor that compresses all images in the working directory.  


### To execute:  
run `gic` in a shell.  
#### To use in your python code:  
A code that the **user** sets the compression level.
```python
import gic.main
#change the working directory to whatever you want
gic.main.run()
```
#### To be quiet:  
A code that **you** set the compression level.
```python
import gic.main
#change the working directory to whatever you want
#set image_quality to 1|2|3|4
gic.main.compress()
```

