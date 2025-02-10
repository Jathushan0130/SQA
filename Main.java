import java.io.File;  // Import the File class
import java.io.FileWriter;   // Import the FileWriter class
import java.io.IOException;  // Import the IOException class to handle errors

public class Main
{
public static void main(String[] args)
{
    //login and logout be done in main
    try{
        File myObj = new File("Bank transaction file");
        if (myObj.createNewFile()) {
        System.out.println("File created: " + myObj.getName());
      } else {
        System.out.println("File already exists.");
    }
    }catch(IOException e){
        System.out.println("An error occurred.");
       e.printStackTrace();

    }

}
public static void withdrawl()
{

}
public static void deposit()
{

}
public static void create()
{

}
public static void changePlan()
{

}
public static void delete()
{

}
public static void disable()
{

}
public static void transfer()
{

}
public static void paybill()
{

}
}