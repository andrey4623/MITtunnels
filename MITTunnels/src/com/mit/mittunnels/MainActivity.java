package com.mit.mittunnels;

import java.util.List;

import android.support.v7.app.ActionBarActivity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends ActionBarActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		final WifiManager wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
        registerReceiver(new BroadcastReceiver() {
                @Override
                public void onReceive(Context c, Intent intent) 
                {
                   List<ScanResult> results = wifiManager.getScanResults();
                   for (ScanResult ap : results) {
                       Log.d("", "SSID=" + ap.SSID + " MAC=" + ap.BSSID+" LEVEL="+ap.level); 
                   }
                }

				
        }, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)); 
        wifiManager.startScan();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
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
