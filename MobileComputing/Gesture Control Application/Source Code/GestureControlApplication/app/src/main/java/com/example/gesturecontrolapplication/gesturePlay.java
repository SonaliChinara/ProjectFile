package com.example.gesturecontrolapplication;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;

import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.VideoView;

import java.util.HashMap;
import java.util.Map;

public class gesturePlay extends AppCompatActivity {

    static final int REQUEST_VIDEO_CAPTURE = 1;
    String strSelectedGesture;
    Map gesVideoMap = null;
    int iReplayCount = 0;

    VideoView gestureVideoView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_gesture_play);

        createGestureVideoMap();

        Intent getGesture = getIntent();
        strSelectedGesture = getGesture.getStringExtra("selectedGesture");
        System.out.println("CS535: Selected gesture in screen 2:::::::::"+strSelectedGesture);

        //Play video based on gesture selection
        playVideo(strSelectedGesture);

        //Navigate to screen 3 to record video
        navigateToRecordVideo();
    }

    //Method to Play video based on gesture selection
    public void playVideo(String gesture){
        int videoFileCode = (int) gesVideoMap.get(gesture);
        String strVideoPath = "android.resource://" + getPackageName() + "/"  + videoFileCode;
        Uri uri = Uri.parse(strVideoPath);

        gestureVideoView = (VideoView) findViewById(R.id.gesture_videoview);
        gestureVideoView.setVideoURI(uri);
        gestureVideoView.start();

        MediaController mediaPlayVideo = new MediaController(this);
        mediaPlayVideo.setAnchorView(gestureVideoView);
        gestureVideoView.setMediaController(mediaPlayVideo);
    }

    //Method to create a key value pair for gesture and corresponding mp4 file
    public void createGestureVideoMap(){
        gesVideoMap = new HashMap<String, String>();
        gesVideoMap.put("Num0",R.raw.h0);
        gesVideoMap.put("Num1",R.raw.h1);
        gesVideoMap.put("Num2",R.raw.h2);
        gesVideoMap.put("Num3",R.raw.h3);
        gesVideoMap.put("Num4",R.raw.h4);
        gesVideoMap.put("Num5",R.raw.h5);
        gesVideoMap.put("Num6",R.raw.h6);
        gesVideoMap.put("Num7",R.raw.h7);
        gesVideoMap.put("Num8",R.raw.h8);
        gesVideoMap.put("Num9",R.raw.h9);
        gesVideoMap.put("LightOn",R.raw.lighton);
        gesVideoMap.put("LightOff",R.raw.lightoff);
        gesVideoMap.put("FanOn",R.raw.fanon);
        gesVideoMap.put("FanOff",R.raw.fanoff);
        gesVideoMap.put("FanUp",R.raw.increasefanspeed);
        gesVideoMap.put("FanDown",R.raw.decreasefanspeed);
        gesVideoMap.put("SetThermo",R.raw.setthermo);
    }

    //Method to replay video
    public void replayVideo(View view) {
        playVideo(strSelectedGesture);
    }

    //Method to navigate to screen 3
    public void navigateToRecordVideo(){
        Button btPractice = findViewById(R.id.practice_button);
        btPractice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intentracticeVideo = new Intent(gesturePlay.this,recordVideo.class);
                intentracticeVideo.putExtra("selectedGesture",strSelectedGesture);
                startActivity(intentracticeVideo);
            }
        });
    }
}