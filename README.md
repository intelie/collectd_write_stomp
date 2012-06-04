
# collectd write_stomp plugin 


## Getting started

1. Install stomppy module
1. Install collectd with python support
1. Configure collectd.conf
1. Copy src/write_stomp.py to collectd's python module

## Installing collectd with python

    sudo aptitude install python2.6-dev
	wget http://collectd.org/files/collectd-5.1.0.tar.bz2
	tar -xjf collectd-5.1.0.tar.bz2 && cd collectd-5.1.0 
	./configure --with-python=/usr/bin/python --prefix=/opt/collectd-5.1
	make && sudo make install

## Installing stomppy module

    wget http://stomppy.googlecode.com/files/stomp.py-3.1.3.tar.gz
    tar -xvzf stomp.py-3.1.3.tar.gz && cd stomp.py-3.1.3
    python setup.py install

## Copying module

     sudo mkdir /opt/collectd-modules
	 cp src/* /opt/collectd-modules


## collectd.conf example

    <LoadPlugin python>
      Globals true
    </LoadPlugin>
    
    <Plugin python>
       ModulePath "/opt/collectd-modules/"
       LogTraces true # debug only
       Interactve true  # debug only
       
       Import "write_stomp"

	   # default values
       <Module write_stomp>
         host "localhost"
         port "61613"
         destination "/queue/messages"
       </Module>
    </Plugin>




	
