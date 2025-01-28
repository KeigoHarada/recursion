abstract class Fly{
    abstract void fly();
    abstract void FlightHeight();
    abstract void FlySpeed();
}

class Bird extends Fly{
    void fly(){
        System.out.println("Bird is flying");
    }
    void FlightHeight(){
        System.out.println("Bird is flying at 1000m");
    }
    void FlySpeed(){
        System.out.println("Bird is flying at 100km/h");
    }
}

class Plane extends Fly{
    void fly(){
        System.out.println("Plane is flying");
    }
    void FlightHeight(){
        System.out.println("Plane is flying at 10000m");
    }
    void FlySpeed(){
        System.out.println("Plane is flying at 1000km/h");
    }
}

public class Main{
    public static void main(String[] args){
        Fly f = new Bird();
        f.fly();
        f.FlightHeight();
        f.FlySpeed();

        f = new Plane();
        f.fly();
        f.FlightHeight();
        f.FlySpeed();
    }
}