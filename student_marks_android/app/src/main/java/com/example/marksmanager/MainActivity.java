package com.example.marksmanager;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.marksmanager.data.MarksRepository;
import com.example.marksmanager.util.PdfUtil;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private EditText nameInput;
    private EditText subjectInput;
    private EditText marksInput;
    private Button addButton;
    private Button pdfButton;
    private RecyclerView recyclerView;
    private RecordsAdapter adapter;
    private MarksRepository repository;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        repository = new MarksRepository(this);

        nameInput = findViewById(R.id.input_name);
        subjectInput = findViewById(R.id.input_subject);
        marksInput = findViewById(R.id.input_marks);
        addButton = findViewById(R.id.btn_add);
        pdfButton = findViewById(R.id.btn_pdf);
        recyclerView = findViewById(R.id.recycler);

        adapter = new RecordsAdapter();
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);

        addButton.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) { onAddClicked(); }
        });
        pdfButton.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) { onPdfClicked(); }
        });

        loadToday();
    }

    private void onAddClicked() {
        String name = nameInput.getText().toString().trim();
        String subject = subjectInput.getText().toString().trim();
        String marksStr = marksInput.getText().toString().trim();
        if (TextUtils.isEmpty(name) || TextUtils.isEmpty(subject) || TextUtils.isEmpty(marksStr)) {
            Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show();
            return;
        }
        double marks;
        try { marks = Double.parseDouble(marksStr); } catch (NumberFormatException ex) {
            Toast.makeText(this, "Marks must be a number", Toast.LENGTH_SHORT).show();
            return;
        }
        String timestamp = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.US).format(new Date());
        repository.insertRecord(name, subject, marks, timestamp);
        nameInput.setText("");
        subjectInput.setText("");
        marksInput.setText("");
        loadToday();
    }

    private void onPdfClicked() {
        String today = new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date());
        List<MarksRepository.Record> records = repository.getRecordsByDate(today);
        if (records.isEmpty()) {
            Toast.makeText(this, "No records for today", Toast.LENGTH_SHORT).show();
            return;
        }
        try {
            PdfUtil.GeneratedPdf generated = PdfUtil.generateDailyReport(this, today, records);
            Intent intent = new Intent(Intent.ACTION_SEND);
            intent.setType("application/pdf");
            intent.putExtra(Intent.EXTRA_STREAM, generated.uri);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivity(Intent.createChooser(intent, "Share PDF"));
        } catch (IOException e) {
            Toast.makeText(this, "Failed to generate PDF: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void loadToday() {
        String today = new SimpleDateFormat("yyyy-MM-dd", Locale.US).format(new Date());
        List<MarksRepository.Record> records = repository.getRecordsByDate(today);
        adapter.submit(records);
    }

    // Simple RecyclerView adapter
    static class RecordsAdapter extends RecyclerView.Adapter<RecordViewHolder> {
        private final List<MarksRepository.Record> items = new ArrayList<>();
        void submit(List<MarksRepository.Record> newItems) {
            items.clear();
            items.addAll(newItems);
            notifyDataSetChanged();
        }
        @Override public RecordViewHolder onCreateViewHolder(android.view.ViewGroup parent, int viewType) {
            android.view.View view = android.view.LayoutInflater.from(parent.getContext()).inflate(R.layout.item_record, parent, false);
            return new RecordViewHolder(view);
        }
        @Override public void onBindViewHolder(RecordViewHolder holder, int position) {
            holder.bind(items.get(position));
        }
        @Override public int getItemCount() { return items.size(); }
    }

    static class RecordViewHolder extends RecyclerView.ViewHolder {
        private final android.widget.TextView title;
        private final android.widget.TextView subtitle;
        RecordViewHolder(android.view.View itemView) {
            super(itemView);
            title = itemView.findViewById(R.id.item_title);
            subtitle = itemView.findViewById(R.id.item_subtitle);
        }
        void bind(MarksRepository.Record r) {
            title.setText(r.studentName + " - " + r.subject + " (" + r.marks + ")");
            String time = r.createdAt.length() >= 16 ? r.createdAt.substring(11,16) : r.createdAt;
            subtitle.setText("#" + r.id + " • " + time);
        }
    }
}
