package com.example.gesturecontrolapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.Button;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, AdapterView.OnItemSelectedListener {

    Button btNext ;
    String strSelectedGesture="";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Show all the gesture in dropdown list
        showGestureList();

        //Navigate to screen 2 to play the selected gesture
        navigateToGesturePlayScreen();
    }

    //Method to show all the gesture in dropdown list
    public void showGestureList(){
        System.out.println("CS535: Executing showGestureList Method::::::::: START");
        Spinner gestureListSpinner  = findViewById(R.id.gesture_spinner);
        ArrayAdapter gestureAdapter = ArrayAdapter.createFromResource(this,R.array.gesture_name,android.R.layout.simple_spinner_dropdown_item);
        gestureAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        gestureListSpinner.setAdapter(gestureAdapter);
        gestureListSpinner.setOnItemSelectedListener(this);
        System.out.println("CS535: Executing showGestureList Method::::::::: END");
    }

    public void navigateToGesturePlayScreen(){
        btNext = findViewById(R.id.next_button);
        btNext.setOnClickListener(this);
    }
    @Override
    public void onClick(View v) {
        Intent myGestureIntent = new Intent(this, gesturePlay.class);
        myGestureIntent.putExtra("selectedGesture",strSelectedGesture);
        startActivity(myGestureIntent);
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        strSelectedGesture = parent.getSelectedItem().toString();
        System.out.println("CS535: Selected gesture in screen 1:::::::::"+strSelectedGesture);
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {
        System.out.println("::----NO VALUE SELECTED----::");

    }
}