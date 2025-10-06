package com.example.marksmanager.data;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class MarksDbHelper extends SQLiteOpenHelper {
    public static final String DB_NAME = "marks.db";
    public static final int DB_VERSION = 1;

    public MarksDbHelper(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(
            "CREATE TABLE IF NOT EXISTS marks (" +
            "id INTEGER PRIMARY KEY AUTOINCREMENT," +
            "student_name TEXT NOT NULL," +
            "subject TEXT NOT NULL," +
            "marks REAL NOT NULL," +
            "created_at TEXT NOT NULL)"
        );
        db.execSQL("CREATE INDEX IF NOT EXISTS idx_marks_date ON marks(substr(created_at,1,10))");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // For MVP, drop and recreate
        db.execSQL("DROP TABLE IF EXISTS marks");
        onCreate(db);
    }
}
