package com.mit.mitlocator;

import java.util.ArrayList;
import java.util.List;

import com.parse.FindCallback;
import com.parse.ParseException;
import com.parse.ParseObject;
import com.parse.ParseQuery;

import android.graphics.Point;

public class MITTunnelsLogic {
	private ArrayList<AccessPoint> _spots;
	private ArrayList<AccessPoint> _scannedAccessPoints;
	private static List<ParseObject>allObjects;
	
	public ArrayList<AccessPoint> getSpots(){
		return _spots;
	}
	
	public MITTunnelsLogic(){
		
		_spots = new ArrayList<AccessPoint>();
		_scannedAccessPoints = new ArrayList<AccessPoint>();
		
		allObjects	= new ArrayList<ParseObject>();
		
	}



public Point getLocationBasedOnAccessPoints(ArrayList scannedAccessPoints){
	return new Point(50,50);
}
}
