# Screenlogic Over IP in Python

I wanted to see how to communicate with my Screenlogic device over IP
instead of through the RS485 bus.

The protocol and codes are documented fairly well here:
https://github.com/ceisenach/screenlogic_over_ip

This code is essentially a translation of https://github.com/parnic/node-screenlogic
into Python. It's not complete because I didn't see an ROI on going further right now,
I just wanted to figure out how to do it. These are more or less my
notes on how to get started should I come back to this. If I do, it'll be to get the
functionality of https://github.com/tagyoureit/nodejs-poolController
over IP instead of RS-485.

The @tagyoureit code is the best I've seen, the only issue I have with it is I don't
like the RS485 interface because it requires a Raspberry Pi physically connected to
the controller (though in theory I could ditch the contoller completely. I seriously
dislike the ScreenLogic app but it is still a little more complete than the nodejs 
solution).

Keith
