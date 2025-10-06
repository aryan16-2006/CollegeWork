package com.example.marksmanager.util;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.pdf.PdfDocument;
import android.net.Uri;
import android.os.Environment;

import androidx.core.content.FileProvider;

import com.example.marksmanager.data.MarksRepository;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.List;

public class PdfUtil {
    public static class GeneratedPdf {
        public final File file;
        public final Uri uri;
        public GeneratedPdf(File file, Uri uri) { this.file = file; this.uri = uri; }
    }

    public static GeneratedPdf generateDailyReport(Context context, String date, List<MarksRepository.Record> records) throws IOException {
        PdfDocument document = new PdfDocument();
        Paint paint = new Paint();
        Paint titlePaint = new Paint();
        titlePaint.setTextSize(18f);
        titlePaint.setFakeBoldText(true);
        paint.setTextSize(12f);

        int pageWidth = 595; // A4 width in points (approx for Android PdfDocument)
        int pageHeight = 842;
        int margin = 24;

        PdfDocument.PageInfo pageInfo = new PdfDocument.PageInfo.Builder(pageWidth, pageHeight, 1).create();
        PdfDocument.Page page = document.startPage(pageInfo);
        Canvas canvas = page.getCanvas();

        int y = margin + 20;
        canvas.drawText("Daily Marks Report - " + date, margin, y, titlePaint);
        y += 24;

        // Header
        canvas.drawText("ID", margin, y, paint);
        canvas.drawText("Name", margin + 40, y, paint);
        canvas.drawText("Subject", margin + 220, y, paint);
        canvas.drawText("Marks", margin + 360, y, paint);
        canvas.drawText("Time", margin + 430, y, paint);
        y += 16;

        DecimalFormat df = new DecimalFormat("0.00");
        double total = 0.0;
        for (MarksRepository.Record r : records) {
            if (y > pageHeight - margin) {
                document.finishPage(page);
                pageInfo = new PdfDocument.PageInfo.Builder(pageWidth, pageHeight, (document.getPages().size()+1)).create();
                page = document.startPage(pageInfo);
                canvas = page.getCanvas();
                y = margin;
            }
            String time = r.createdAt.length() >= 16 ? r.createdAt.substring(11,16) : r.createdAt;
            canvas.drawText(String.valueOf(r.id), margin, y, paint);
            canvas.drawText(r.studentName, margin + 40, y, paint);
            canvas.drawText(r.subject, margin + 220, y, paint);
            canvas.drawText(df.format(r.marks), margin + 360, y, paint);
            canvas.drawText(time, margin + 430, y, paint);
            y += 16;
            total += r.marks;
        }
        int count = records.size();
        double avg = count == 0 ? 0.0 : total / count;
        y += 8;
        canvas.drawText("Total Records: " + count + "   Average: " + df.format(avg), margin, y, paint);

        document.finishPage(page);

        File reportsDir = new File(context.getFilesDir(), "reports");
        if (!reportsDir.exists()) reportsDir.mkdirs();
        File pdfFile = new File(reportsDir, "marks_report_" + date + ".pdf");
        FileOutputStream fos = new FileOutputStream(pdfFile);
        document.writeTo(fos);
        fos.close();
        document.close();

        Uri uri = FileProvider.getUriForFile(context, context.getPackageName() + ".fileprovider", pdfFile);
        return new GeneratedPdf(pdfFile, uri);
    }
}
