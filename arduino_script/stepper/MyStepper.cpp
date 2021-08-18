#include "MyStepper.h"
#include "DirectAccess.h"

Stepper::Stepper(uint8_t pul_pin, uint8_t dir_pin){
    _pul_pin = pul_pin;
    _dir_pin = dir_pin;
    
    _currentPos = 0;
    _direction = 0;

    _step_interval = 10; // us

    initOutputPin(_pul_pin);
    initOutputPin(_dir_pin);

    setOutputPin(pul_pin, LOW);
}

void Stepper::reset(uint8_t enable_pin){
    pinMode(enable_pin, INPUT);
    setDirection(HIGH); 
    while(not readPin(enable_pin)){
        delayMicroseconds(_step_interval);
        step();
    }
    setPosition(0); // set one boundary as 0 position.
    delay(500);

    setDirection(LOW);
    _max_dist_from_0 = 0;
    while(not readPin(enable_pin)){
        delayMicroseconds(_step_interval);
        step();
        _max_dist_from_0 += 1;
    }
    _max_dist_from_0 /= 2;
        
    setPosition(_max_dist_from_0); // set centre as 0 position.
    moveTo(0);
    while (distanceToGo() != 0)
        run();
    _bound_set = true;
}

void Stepper::moveTo(long absolute){
    _targetPos = absolute;
    long displacement = _targetPos - _currentPos;
    if (displacement > 0)
        setDirection(LOW);
    else if (displacement < 0)
        setDirection(HIGH);
}

void Stepper::setDirection(bool direction){
    _direction = direction;
    setOutputPin(_dir_pin, _direction);
}

void Stepper::setSpeed(unsigned int speed){
    float period = 1e6/speed;
    if (period - _pulse_width < 0)
        _step_interval = 0;
    else
        _step_interval = (unsigned int) (period - _pulse_width);
}

void Stepper::setPulseWidth(unsigned int width){
    _pulse_width = width;
}


void Stepper::run(){
    if (_currentPos != _targetPos){
        /* if (_bound_set && abs(_currentPos) <= _max_dist_from_0) */
        /*     return; */
        step();
        _currentPos += _direction ? -1 : 1;
        /* delayMicroseconds(_step_interval); */
    }
}

void Stepper::step(){
    setOutputPin(2, HIGH);
    delayMicroseconds(_pulse_width); 
    setOutputPin(2, LOW);
}

long Stepper::getPosition(){
    return _currentPos;
}

long Stepper::distanceToGo(){
    return _targetPos - _currentPos;
}

void Stepper::setPosition(long pos){
    _currentPos = pos; 
}

