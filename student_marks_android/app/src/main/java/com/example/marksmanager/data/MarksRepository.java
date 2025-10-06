package com.example.marksmanager.data;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import java.util.ArrayList;
import java.util.List;

public class MarksRepository {
    private final MarksDbHelper dbHelper;

    public static class Record {
        public long id;
        public String studentName;
        public String subject;
        public double marks;
        public String createdAt; // ISO8601
    }

    public MarksRepository(Context context) {
        dbHelper = new MarksDbHelper(context.getApplicationContext());
    }

    public long insertRecord(String name, String subject, double marks, String timestampIso) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put("student_name", name);
        values.put("subject", subject);
        values.put("marks", marks);
        values.put("created_at", timestampIso);
        return db.insert("marks", null, values);
    }

    public List<Record> getRecordsByDate(String yyyyMmDd) {
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        String[] cols = new String[]{"id","student_name","subject","marks","created_at"};
        String sel = "substr(created_at,1,10) = ?";
        String[] selArgs = new String[]{yyyyMmDd};
        Cursor c = db.query("marks", cols, sel, selArgs, null, null, "created_at ASC");
        List<Record> results = new ArrayList<>();
        try {
            while (c.moveToNext()) {
                Record r = new Record();
                r.id = c.getLong(0);
                r.studentName = c.getString(1);
                r.subject = c.getString(2);
                r.marks = c.getDouble(3);
                r.createdAt = c.getString(4);
                results.add(r);
            }
        } finally {
            c.close();
        }
        return results;
    }
}
