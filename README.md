# Desktop Application for Normalization of Fiber Reinforced Composites

Here is a simple desktop application to calculate the normalized values of uniaxial tensile/compression test data of fiber reinforced composites (FRC).

The raw test data after either uniaxial tensile or uniaxial compression test must be normalized with a specific fiber volume fraction. The reason of this practice is to equally evaluate the mechanical behavior of FRCs panels regardless of fiber volume fraction due to possible variations that may occur in different batches (for further information: [Composite Materials Handbook ](https://apps.dtic.mil/sti/pdfs/ADA426516.pdf)).

This desktop application takes raw test data and normalizes it by using the actual fiber volume fraction measured from the cross-section image of the sample, taken by optical microscope or SEM (scanning electron microscope). After uploading the raw data, a database file is generated in SQL format and all data is transferred to this database. Later on, the data is fetched from this database to be used in the calculations. After uploading the cross-section image, the fiber content is found by using Binary and Triangle threshold algorithms in OpenCV library. According to normalizing volume fraction given by the user, the tensile strength and the elastic modulus is calculated according to ASTM D3039 test standard. These values are shown in a separate window together with actual volume fraction of the sample.  

In terms of engineering and practical aspect, this kind of application may enable easier and faster calculation of the normalized mechanical properties and the volume fraction, which are critical design variables for a structural part, during manufacturing and quality control operations. If the samples are inspected by microstructure examination during production, calculating these values by utilizing this application may save material and time costs in addition to enabling easier calculations by minimizing the human input and automating the process.

I had started this project 3 years ago when I took a course on Python. In this project, I aimed to practice PyQT5 for GUI creation, OpenCV for image analysis, SQlite for database management together with object-oriented programming (OOP).

The steps showing how the application works are shown in the workflow below.
<p align="center">
  <img width="400" src="/workflow.png"/>
</p>

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
