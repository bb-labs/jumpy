FROM lambci/lambda:build-python3.7

RUN git clone https://github.com/bb-labs/jumpy.git
RUN pip install numpy
RUN cp -r /var/lang/lib/python3.7/site-packages/numpy ./jumpy/src/back
