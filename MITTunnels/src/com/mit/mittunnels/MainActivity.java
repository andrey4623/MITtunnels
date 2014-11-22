package com.mit.mittunnels;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import com.larvalabs.svgandroid.SVG;
import com.larvalabs.svgandroid.SVGParser;
import com.parse.FindCallback;
import com.parse.Parse;
import com.parse.ParseException;
import com.parse.ParseObject;
import com.parse.ParseQuery;
import com.parse.SaveCallback;

import android.support.v7.app.ActionBarActivity;
import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Bitmap;
import android.graphics.Bitmap.Config;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.graphics.Rect;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.PictureDrawable;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;

public class MainActivity extends ActionBarActivity {

	private static final int SWIPE_THRESHOLD = 1;
	private static final int SWIPE_VELOCITY_THRESHOLD = 1;
	private static final int SWIPE_VELOCITY_MAPMOVE = 30;
	private static int CURRENT_VIEW_WIDTH = 400;
	private static int CURRENT_VIEW_HEIGHT = 400;

	private float currentx, currenty;
	private Button btnSaveLocation;
	//private Button btnGetLocation;
	private Button btnMoveRight;
	private Button btnZoomIn;
	private Button btnZoomOut;
	private ImageView imageView;
	private int leftPos = 0;
	private boolean isMapMoving = false;
	private Point pointStart;
	private Point pointCurrent;
	//private TextView textViewDevelopers;

	private int mapMaxWidth = 640;
	private int mapMaxHeight = 480;

	private int x = 250;
	private int y = 250;

	/** Called when the user touches the button */
	public void moveMapRight(View view) {
		// Do something in response to button click

		// if (leftPos+310<500)

		onSwipeTop();
	}

	public void checkBorders() {
		if (x < (int) CURRENT_VIEW_WIDTH / 2)
			x = (int) CURRENT_VIEW_WIDTH / 2;
		if (x > mapMaxWidth - (int) CURRENT_VIEW_WIDTH / 2)
			x = mapMaxWidth - (int) CURRENT_VIEW_WIDTH / 2;
		if (y < (int) CURRENT_VIEW_HEIGHT / 2)
			y = (int) CURRENT_VIEW_HEIGHT / 2;
		if (y > mapMaxHeight - (int) CURRENT_VIEW_HEIGHT / 2)
			y = mapMaxHeight - (int) CURRENT_VIEW_HEIGHT / 2;
	}

	private void zoomIn() {
		if (CURRENT_VIEW_WIDTH <= 100)
			return;
		CURRENT_VIEW_WIDTH -= 100;
		CURRENT_VIEW_HEIGHT -= 100;
		drawMap();
	}

	private void zoomOut() {
		if (CURRENT_VIEW_WIDTH >= 600)
			return;
		if (CURRENT_VIEW_WIDTH >= mapMaxWidth)
			return;
		CURRENT_VIEW_WIDTH += 100;
		CURRENT_VIEW_HEIGHT += 100;
		drawMap();
	}

	public void onSwipeRight() {
		x -= SWIPE_VELOCITY_MAPMOVE;
		checkBorders();
		drawMap();
	}

	public void onSwipeLeft() {
		x += SWIPE_VELOCITY_MAPMOVE;
		checkBorders();
		drawMap();
	}

	public void onSwipeTop() {
		y += SWIPE_VELOCITY_MAPMOVE;
		checkBorders();
		drawMap();
	}

	public void onSwipeBottom() {
		y -= SWIPE_VELOCITY_MAPMOVE;
		checkBorders();
		drawMap();
	}

	private PictureDrawable pictureDrawable = null;
	Bitmap bitmap;
	Canvas canvas;

	private void drawMap() {

		if (pictureDrawable == null)
			return;

		// crop the bitmap
		// we are at x1,y1
		int x1 = x - (int) CURRENT_VIEW_WIDTH / 2;
		int y1 = y - (int) CURRENT_VIEW_HEIGHT / 2;
		int x2 = x + (int) CURRENT_VIEW_WIDTH / 2;
		int y2 = y + (int) CURRENT_VIEW_HEIGHT / 2;

		// exit from the map

		if (x1 < 0)
			x1 = 0;
		if (x1 > mapMaxWidth)
			x1 = mapMaxWidth - 1;
		if (y1 < 0)
			y1 = 0;
		if (y1 > mapMaxHeight)
			y1 = mapMaxHeight - 1;

		String str = Integer.toString(x1) + " " + Integer.toString(y1) + " "
				+ Integer.toString(x2) + " " + Integer.toString(y2) + " ";
		//textViewDevelopers.setText(str);
		Bitmap yourBitmap = Bitmap.createBitmap(bitmap, x1, y1, x2 - x1, y2
				- y1);
		Bitmap tempBitmap = Bitmap.createBitmap(CURRENT_VIEW_WIDTH,
				CURRENT_VIEW_HEIGHT, Bitmap.Config.ARGB_8888);

		Bitmap largeWhiteBitmap = Bitmap.createBitmap(CURRENT_VIEW_WIDTH,
				CURRENT_VIEW_HEIGHT, Bitmap.Config.ARGB_8888);
		Canvas yourcanvas = new Canvas(largeWhiteBitmap);
		yourcanvas.drawColor(0xffffffff);

		yourcanvas.drawBitmap(yourBitmap, 0, 0, new Paint());

		imageView.setImageBitmap(largeWhiteBitmap);
	}

	private void loadMap() {
		SVG svg = SVGParser.getSVGFromString(readMapFromFile());
		pictureDrawable = svg.createPictureDrawable();
		bitmap = Bitmap.createBitmap(500, 500, Config.ARGB_8888);
		canvas = new Canvas(bitmap);
		canvas.drawPicture(pictureDrawable.getPicture());
	}

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		// Parse initialize
		Parse.initialize(this, "dqqy2pgILHlRNjtKu5MLi4VyY0LkZJY27FgrufLh",
				"fSFmvqwVMeuhsuzavaa7KJAMg5XDPhN0CcjTDiFE");

		btnSaveLocation = (Button) findViewById(R.id.btnSaveLocation);
		//btnGetLocation = (Button) findViewById(R.id.btnGetLocation);
		btnMoveRight = (Button) findViewById(R.id.btnZoomIn);
		btnZoomIn = (Button) findViewById(R.id.btnZoomIn);
		btnZoomOut = (Button) findViewById(R.id.btnZoomOut);
		imageView = (ImageView) findViewById(R.id.imgMap);
		pointStart = new Point();
		pointCurrent = new Point();

		//textViewDevelopers = (TextView) findViewById(R.id.txtViewInstructions);
		loadMap();// load the svg file

		mapMaxWidth = 500;
		mapMaxHeight = 500;

		

		/*
		 * btnSaveLocation.setOnClickListener(new View.OnClickListener() {
		 * public void onClick(View v) { // Do something in response to button
		 * click
		 * 
		 * 
		 * } });
		 */

		btnZoomIn.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				// Do something in response to button click
				zoomIn();
			}
		});

		btnZoomOut.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				// Do something in response to button click
				zoomOut();
			}
		});

		btnSaveLocation.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				// get list of network

				final WifiManager wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
				registerReceiver(new BroadcastReceiver() {
					@Override
					public void onReceive(Context c, Intent intent) {
						List<ScanResult> results = wifiManager.getScanResults();
						for (ScanResult ap : results) {

							ParseObject testObject = new ParseObject(
									"ScanResult");
							testObject.put("x", Float.toString(currentx));
							testObject.put("y", Float.toString(currenty));
							testObject.put("SSID", ap.SSID);
							testObject.put("MAC", ap.BSSID);
							testObject.put("LEVEL", ap.level);

							testObject.saveInBackground(new SaveCallback() {
								public void done(ParseException e) {
									if (e == null) {
										// myObjectSavedSuccessfully();

									} else {

									}
								}
							});

							// testObject.saveInBackground();
							Log.d("", "SSID=" + ap.SSID + " MAC=" + ap.BSSID
									+ " LEVEL=" + ap.level);

						}
					}

				}, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
				wifiManager.startScan();

			}
		});

		imageView.setOnTouchListener(new View.OnTouchListener() {

			@Override
			public boolean onTouch(View v, MotionEvent event) {

				// The following code set pointer
				/*
				 * Bitmap bmp =
				 * Bitmap.createBitmap(imageView.getMeasuredWidth(),
				 * imageView.getMeasuredHeight(), Config.ARGB_8888);
				 * imageView.setBackgroundResource
				 * (R.drawable.fivefloorplanproject); Canvas c = new
				 * Canvas(bmp);
				 * 
				 * Paint p = new Paint(); int color = Color.WHITE;
				 * p.setColor(color);
				 * 
				 * color = Color.RED; p.setColor(color); currentx =
				 * event.getX(); currenty = event.getY(); //c.drawBitmap(bmp,
				 * 300, 300, p); c.drawCircle(event.getX(), event.getY(), 10,
				 * p);
				 * 
				 * imageView.setImageBitmap(bmp);
				 */

				int action = event.getAction();
				switch (action) {

				case MotionEvent.ACTION_DOWN:

					isMapMoving = true;

					pointStart.x = (int) event.getX();
					pointStart.y = (int) event.getY();

					break;

				case MotionEvent.ACTION_MOVE:

					if (isMapMoving) {

						pointCurrent.x = (int) event.getX();
						pointCurrent.y = (int) event.getY();

						try {
							int diffY = pointCurrent.y - pointStart.y;
							int diffX = pointCurrent.x - pointStart.x;

							pointStart.x = (int) event.getX();
							pointStart.y = (int) event.getY();

							if (Math.abs(diffX) > Math.abs(diffY)) {
								if (Math.abs(diffX) > SWIPE_THRESHOLD) {
									if (diffX > 0) {
										onSwipeRight();
									} else {
										onSwipeLeft();
									}
								}

							} else if (Math.abs(diffY) > SWIPE_THRESHOLD) {
								if (diffY > 0) {
									onSwipeBottom();
								} else {
									onSwipeTop();
								}
							}

						} catch (Exception exception) {
							exception.printStackTrace();
						}

					}

					break;

				case MotionEvent.ACTION_UP:
					isMapMoving = false;

					imageView.invalidate();
					break;
				}
				return true;
			}

		});

		//btnGetLocation.setOnClickListener(new View.OnClickListener() {
		//	public void onClick(View v) {

				/*
				 * 
				 * final ArrayList<AccessPoint> arrayList = new
				 * ArrayList<AccessPoint>();
				 * 
				 * final WifiManager wifiManager = (WifiManager)
				 * getSystemService(Context.WIFI_SERVICE); registerReceiver(new
				 * BroadcastReceiver() {
				 * 
				 * @Override public void onReceive(Context c, Intent intent) {
				 * List<ScanResult> results = wifiManager.getScanResults(); for
				 * (ScanResult ap : results) {
				 * 
				 * 
				 * AccessPoint app = new AccessPoint(); app.MAC = ap.BSSID;
				 * app.LEVEL = ap.level; arrayList.add(app);
				 * 
				 * 
				 * 
				 * }
				 * 
				 * 
				 * //sort list int size = arrayList.size(); for (int i=0; i<
				 * arrayList.size()-1; i++) for (int j=0; j< arrayList.size()-1;
				 * j++) {
				 * 
				 * AccessPoint app1 = arrayList.get(i); AccessPoint app2 =
				 * arrayList.get(i+1);
				 * 
				 * if (app2.LEVEL<app1.LEVEL) { AccessPoint toMove =
				 * arrayList.get(i); arrayList.set(i, arrayList.get(i-1));
				 * arrayList.set(i-1, toMove); }
				 * 
				 * }
				 * 
				 * //find in the cloud int a=1; a=2; String tempm =
				 * arrayList.get(0).MAC;
				 * 
				 * 
				 * ParseQuery<ParseObject> query =
				 * ParseQuery.getQuery("ScanResult"); query.whereEqualTo("MAC",
				 * tempm);
				 * 
				 * query.findInBackground(new FindCallback<ParseObject>() {
				 * public void done(List<ParseObject> scoreList, ParseException
				 * e) { if (e == null) { String x =
				 * scoreList.get(0).getString("x"); String y =
				 * scoreList.get(0).getString("y");
				 * 
				 * float fl_x = Float.parseFloat(x); float fl_y =
				 * Float.parseFloat(y);
				 * 
				 * drawPointOnGivenLocation(fl_x, fl_y);
				 * 
				 * 
				 * 
				 * 
				 * 
				 * 
				 * Log.d("score", "Retrieved " +
				 * scoreList.get(0).getString("x")+
				 * " "+scoreList.get(0).getString("y")); } else { Log.d("score",
				 * "Error: " + e.getMessage()); } } });
				 * 
				 * 
				 * }
				 * 
				 * 
				 * }, new
				 * IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
				 * wifiManager.startScan();
				 */

			//}

		//});

		
		
		//show the map 
		x = (int)mapMaxWidth/2;
		y = (int)mapMaxHeight/2;
		drawMap();
		
	}
	
	

	public String readMapFromFile() {
		StringBuffer datax = new StringBuffer("");
		try {
			InputStream is = this.getResources().openRawResource(R.raw.map);

			InputStreamReader isr = new InputStreamReader(is);
			BufferedReader buffreader = new BufferedReader(isr);

			String readString = buffreader.readLine();
			while (readString != null) {
				datax.append(readString);
				readString = buffreader.readLine();
			}

			isr.close();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
		return datax.toString();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	private void drawPointOnGivenLocation(float x, float y) {
		Bitmap bmp = Bitmap.createBitmap(imageView.getMeasuredWidth(),
				imageView.getMeasuredHeight(), Config.ARGB_8888);
		imageView.setBackgroundResource(R.drawable.fivefloorplanproject);
		Canvas c = new Canvas(bmp);

		Paint p = new Paint();
		int color = Color.WHITE;
		p.setColor(color);

		color = Color.RED;
		p.setColor(color);
		c.drawCircle(x, y, 10, p);

		imageView.setImageBitmap(bmp);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
}
