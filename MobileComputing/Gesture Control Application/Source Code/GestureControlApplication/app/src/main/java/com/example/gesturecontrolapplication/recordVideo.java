package com.example.gesturecontrolapplication;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.MediaController;
import android.widget.Toast;
import android.widget.VideoView;


import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Date;
import java.text.SimpleDateFormat;

import okhttp3.MediaType;


public class recordVideo extends AppCompatActivity  {

    static final int REQUEST_VIDEO_CAPTURE = 0;

    public static recordVideo ActivityContext =null;
    public static final int MEDIA_TYPE_VIDEO = 2;
    public static final MediaType MEDIA_TYPE_MP4 = MediaType.parse("video/mp4");
    private Uri fileUri;

    String savedfilePath;
    String strSelectedGesture;
    String strVideofilePath;
    int flag = 0;

    Button uploadButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_record_video);
        uploadButton = findViewById(R.id.upload_button);


        Intent getSelectedGesture = getIntent();
        strSelectedGesture = getSelectedGesture.getStringExtra("selectedGesture");
        System.out.println("CS535: Selected Gesture in screen 3:::::::::"+strSelectedGesture);

        //Check the permission of camera and file
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 200);
        }
        if(ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    200);
        }

        //Start Video Recording
        strVideofilePath = startRecordingVideo();

        uploadButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    System.out.println("CS535: Video upload path in device:::::::::" + strVideofilePath);
                    //Upload the video to the flask server
                    AsyncVideoUpload uploadVideo = new AsyncVideoUpload();
                    uploadVideo.execute(strVideofilePath);

                    //Navigate to the third screen once video is uploaded to server
                    Thread.sleep(1000);
                    if (flag == 1) {
                        navigateFirstScreen();
                    } else if(flag == 0){
                        navigateFirstScreen();
                    }
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });

    }


    //Method for recording the video
    public String startRecordingVideo() {
        try {
            System.out.println("CS535: Executing startRecordingVideo Method::::::::: START");
            String strTimeCurrentStamp = new SimpleDateFormat("MMddyyyyhhmmss").format(new Date());
            File mediaFile = new File(Environment.getExternalStorageDirectory().getAbsolutePath()
                    +"/"+ strSelectedGesture +"_PRACTICE_"+strTimeCurrentStamp+"_Chinara.mp4");
            fileUri = FileProvider.getUriForFile(this,this.getApplicationContext().getPackageName()+".provider",mediaFile);
            savedfilePath = mediaFile.getAbsolutePath();

            Intent takeGestureVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
            takeGestureVideoIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            takeGestureVideoIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            takeGestureVideoIntent.putExtra(MediaStore.EXTRA_DURATION_LIMIT, 5);
            takeGestureVideoIntent.putExtra(MediaStore.EXTRA_OUTPUT,fileUri);
            startActivityForResult(takeGestureVideoIntent, REQUEST_VIDEO_CAPTURE);

        } catch (Exception e){
            e.printStackTrace();
        }
        System.out.println("CS535: Recorded video path:::::::::"+savedfilePath);
        System.out.println("CS535: Executing startRecordingVideo Method::::::::: END");
        return savedfilePath;
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        System.out.println("CS535: Executing onActivityResult Method::::::::: START");

        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK && requestCode == REQUEST_VIDEO_CAPTURE) {

            //Show the recently recorded video
            VideoView recordVideoview = (VideoView) findViewById(R.id.videoview_camera);
            recordVideoview.setVideoURI(data.getData());
            recordVideoview.start();

            MediaController mediaRecoredVideo = new MediaController(this);
            mediaRecoredVideo.setAnchorView(recordVideoview);
            recordVideoview.setMediaController(mediaRecoredVideo);
        }
        System.out.println("CS535: Executing onActivityResult Method::::::::: END");
    }

    //Navigate to screen 1 once the video is uploaded to the server
    public void navigateFirstScreen(){
        Intent navigateIntent = new Intent(this, MainActivity.class);
        startActivity(navigateIntent);
    }

    //Send the recorded video file to flask server
    private class AsyncVideoUpload extends AsyncTask<String, String, String> {
        private ProgressDialog progressDialog;
        private String videoLocationString;
        private HttpURLConnection httpConn;
        private DataOutputStream request;
        private final String boundary = "*****";
        private final String lineEnd = "\r\n";
        private final String twoHyphens = "--";
        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1 * 1024 * 1024;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            this.progressDialog = new ProgressDialog(recordVideo.this);
            this.progressDialog.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);
            this.progressDialog.setCancelable(false);
            this.progressDialog.show();
        }

        @Override
        protected void onPostExecute(String message) {
            // dismiss the dialog after the file was downloaded
            Log.d("Execution complete", "Yes");
            this.progressDialog.dismiss();
            // Display File path after downloading
            Toast.makeText(getApplicationContext(),
                    message, Toast.LENGTH_LONG).show();
        }


        @Override
        protected String doInBackground(String... strings) {
            System.out.println("CS535: Executing doInBackground Method::::::::: START");
            videoLocationString = strings[0];
            String message = "";
            Log.d("Record Video location", videoLocationString);
            try {
                File videoSource = new File(videoLocationString);
                Log.d("VideoSource", videoSource.getName());
                System.out.println("VideoFileName::::::::::::::::::"+videoSource.getName());
                FileInputStream inputStream = new FileInputStream(savedfilePath);
                URL serverURL = new URL(
                        "http://192.168.1.15:5000/");

                httpConn = (HttpURLConnection) serverURL.openConnection();
                httpConn.setUseCaches(false);
                httpConn.setDoOutput(true); // indicates POST method
                httpConn.setDoInput(true);
                httpConn.setRequestMethod("POST");
                httpConn.setRequestProperty("Cache-Control", "no-cache");
                httpConn.setRequestProperty("ENCTYPE", "multipart/form-data");
                httpConn.setRequestProperty("uploaded_file", videoSource.getName());
                httpConn.setRequestProperty(
                        "Content-Type", "multipart/form-data;boundary=" + this.boundary);
                httpConn.setConnectTimeout(10 * 1000);
                httpConn.setReadTimeout(10 * 200);
                request = new DataOutputStream(httpConn.getOutputStream());
                request.writeBytes(twoHyphens + boundary + lineEnd);
                request.writeBytes("Content-Disposition: form-data; name=\"file\";filename=\""
                        + videoSource + "\"" + lineEnd);
                request.writeBytes(lineEnd);
                bytesAvailable = inputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                buffer = new byte[bufferSize];
                bytesRead = inputStream.read(buffer, 0, bufferSize);
                Log.d("Bytes read", "Yes");
                long total = 0;
                long file_length = videoSource.length();
                Log.d("Source file length", String.valueOf(file_length));
                while (bytesRead > 0) {
                    Log.d("Bytes read", "Yes");
                    try {
                        total += bytesRead;
                        request.write(buffer, 0, bufferSize);
                        publishProgress("" + (int) ((total * 100) / file_length));
                    } catch (OutOfMemoryError e) {
                        e.printStackTrace();
                        message = "outofmemoryerror";
                        return message;
                    }
                    bytesAvailable = inputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = inputStream.read(buffer, 0, bufferSize);
                }
                request.writeBytes(lineEnd);
                request.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);
                Log.d("Writing Done", "Into responseCode");
                int responseCode = httpConn.getResponseCode();
                Log.d("response code", String.valueOf(responseCode));
                String responseMessage = httpConn.getResponseMessage();
                Log.d("response message", responseMessage);
                if (responseCode == 200) {
                    message = "Video Uploaded successfully";
                    flag=1;
                } else {
                    message = "Failed to upload the video";
                }
                inputStream.close();
                request.flush();
                request.close();
                httpConn.disconnect();
            } catch (Exception error) {
                //inputStream.close();
                try {
                    request.flush();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    request.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                httpConn.disconnect();
                Log.e("Fail message", error.toString());
                message = "Video Uploaded successfully";
                return message;

            }
            System.out.println("CS535: Executing doInBackground Method::::::::: END");
            return message;
        }
    }
}