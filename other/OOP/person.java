enum Denomination {
    heightFirst,
    dollars,
    twenties
}

class Wallet{
    public int bill1;
    public int bill5;
    public int bill10;
    public int bill20;
    public int bill50;
    public int bill100;

    public Wallet(){}

    public int getTotalMoney(){
        return (1*bill1) + (5*bill5) + (10*bill10) + (20*bill20) + (50*bill50) + (100*bill100);
    }

    public int insertBill(int bill, int amount){
        switch(bill){
            case(1):
                bill1 += amount;
                break;
            case(5):
                bill5 += amount;
                break;
            case(10):
                bill10 += amount;
                break;
            case(20):
                bill20 += amount;
                break;
            case(50):
                bill50 += amount;
                break;
            case(100):
                bill100 += amount;
                break;
            default:
                return 0;
        }

        return bill*amount;
    }

    public int removeBill(int bill, int amount){
        switch(bill){
            case(1):
                bill1 -= amount;
                break;
            case(5):
                bill5 -= amount;
                break;
            case(10):
                bill10 -= amount;
                break;
            case(20):
                bill20 -= amount;
                break;
            case(50):
                bill50 -= amount;
                break;
            case(100):
                bill100 -= amount;
                break;
            default:
                return 0;
        }

        return bill*amount;
    }
}

class Person{
    public String firstName;
    public String lastName;
    public int age;
    public double heightM;
    public double weightKg;
    public Wallet wallet;
    private Denomination denomination;

    private static final int[] BILLS = {1, 5, 10, 20, 50, 100};

    public Person(String firstName, String lastName, int age, double heightM, double weightKg){
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.heightM = heightM;
        this.weightKg = weightKg;
        this.wallet = new Wallet();
        this.denomination = Denomination.heightFirst;
    }

    public int getCash(){
        if(this.wallet == null) return 0;
        return this.wallet.getTotalMoney();
    }

    public void printState(){
        System.out.println("firstname - " + this.firstName);
        System.out.println("lastname - " + this.lastName);
        System.out.println("age - " + this.age);
        System.out.println("height - " + this.heightM);
        System.out.println("weight - " + this.weightKg);
        System.out.println("Current Money - " + this.getCash());
        System.out.println();
    }

    public int[] getPayed(int money){
        int[] billCounts = this.calcBillCounts(money);
        for(int i = 0; i < billCounts.length; i++){
            this.wallet.insertBill(i, billCounts[i]);
        }
        return billCounts;
    }

    public int[] spendMoney(int money){
        int[] billCounts = this.calcBillCounts(money);
        for(int i = 0; i < billCounts.length; i++){
            this.wallet.removeBill(i, billCounts[i]);
        }
        return billCounts;
    }

    public void addWallet(Wallet wallet){
        this.wallet = wallet;
    }

    public Wallet dropWallet(){
        Wallet wallet = this.wallet;
        this.wallet = null;
        return wallet;
    }

    public void setDenominationPreference(String denomination){
        switch(denomination){
            case("highestFirst"):
                this.denomination = Denomination.heightFirst;
                break;
            case("dollars"):
                this.denomination = Denomination.dollars;
                break;
            case("twenties"):
                this.denomination = Denomination.twenties;
                break;
            default:
                break;
        }
    }

    private int[] calcBillCounts(int money) {
        int[] counts = new int[6];
        
        switch(this.denomination) {
            case heightFirst:
                return calcHighestFirst(money);
            case dollars:
                return calcDollarsOnly(money);
            case twenties:
                return calcTwentiesPreferred(money);
            default:
                return counts;
        }
    }

    private int[] calcHighestFirst(int remainingMoney) {
        int[] counts = new int[6];
        int money = remainingMoney;
        
        for(int i = BILLS.length - 1; i >= 0; i--) {
            counts[i] = money / BILLS[i];
            money = money % BILLS[i];
        }
        return counts;
    }

    private int[] calcDollarsOnly(int money) {
        int[] counts = new int[6];
        counts[0] = money;  // 1ドル札のみ使用
        return counts;
    }

    private int[] calcTwentiesPreferred(int remainingMoney) {
        int[] counts = new int[6];
        int money = remainingMoney;
        
        // まず20ドル札を優先的に使用
        counts[3] = money / BILLS[3];  // 20ドル札
        money = money % BILLS[3];
        
        // 残りの金額を最大額から順に計算
        for(int i = BILLS.length - 1; i >= 0; i--) {
            if(i != 3) { // 20ドル札以外を処理
                counts[i] = money / BILLS[i];
                money = money % BILLS[i];
            }
        }
        return counts;
    }
}

class Main{
    public static void main(String[] args){
        Person p = new Person("Ryu","Poolhopper", 40, 1.8, 140);
        p.printState();

        p.wallet.insertBill(5,3);
        p.wallet.insertBill(100,2);

        p.printState();
    }
}