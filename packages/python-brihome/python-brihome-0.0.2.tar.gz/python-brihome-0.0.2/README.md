# python-brihome

This library aims to control the brihome smart light bulbs.
It internally uses the pytuya library and is able to control
many parameters on the led bulb.

### Docs
For an example see [examples](examples/rgb.py).

### FAQ
In Order to use the `brihome.Bulb(...)` constructor you need
to obtain the **local device id** and the **device key** that 
your bulb uses. You can find these by sniffing the brihome app's 
traffic. 

### Contributing
Pull request are welcome. Not every function the bulb supports are
implemented. Help on error handling and extended functionality
is welcome.
