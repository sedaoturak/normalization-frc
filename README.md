# Desktop Application for Normalization of Fiber Reinforced Composites

Here is a simple desktop application to calculate the normalized values of uniaxial tensile/compression test data of fiber reinforced composites (FRC).

The raw test data after either uniaxial tensile or uniaxial compression tests must be normalized with a specific fiber volume fraction. The reason of this practice is to equally evaluate the mechanical behavior of FRCs regardless of fiber volume fraction due to possible variations in different batches.

This desktop application takes raw test data and normalizes it by using the actual fiber volume fraction measured from the cross-section image of the sample, taken by optical microscope or SEM. After uploading the raw data, a database file is generated in SQL format and all data is transferred here. Later on, the data is fetched from this database when needed for the calculations. After uploading the cross-section image. the fiber content is found by Binary and Triangle threshold algorithms in OpenCV. According to given normalizing volume fraction by the user, the tensile strength and the elastic modulus is calculated according to ASTM D3039 test standard. These values are shown in a separate window together with actual volume fraction of the sample.  

By doing so, I aimed to practice PyQT5 for GUI creation, OpenCV for image analysis, SQlite for database management together with object-oriented programming (OOP) after taking a course on Python 3 years ago. In terms of engineering and practical aspect, if the samples are inspected by microsstructure for some reason for an appllication, the normalized values and the volume fraction (critical design variables for a structural part) can be easily calculated by this kind of app without performing chemical method to find the volume fraction of the sample, which causes several days and material cost in general.

# How to Use
After installing the dependencies in `requirements.txt` (which only consists of PyQt5, numpy and matplotlib), run `main.py` file. A window shown below will appear. 

1. Upload the test data (the file should be in csv format and the headers of the columns should be "Strain" and "Stress".)
2. Upload the cross section image of the sample
3. Enter the fiber volume fraction at which the normalization will be done (be sure press OK)
4. Press "Normalize" button


<p float="center">
  <img src="/1.png" width="340" />
  <img src="/2.png" width="340" /> 
  <img src="/3.png" width="340" />
</p>

# TODO
- Embedding the windows for the plot of normalized stress-strain and the normalized values in the main window
- Tick sign for uploaded files
- Option for different file formats
- Fetching the data in the original file regardless of the column headers
- Error messages for wrong file formats or actions
