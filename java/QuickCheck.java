import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.time.LocalDateTime;
import java.util.*;

public class QuickCheck {

    public static void main(String[] args) {
        StringBuilder report = new StringBuilder();

        report.append("Linux Security QuickCheck (Java)\n");
        report.append("Generated: ").append(LocalDateTime.now()).append("\n\n");

        // Basic system info
        report.append("== System Info ==\n");
        report.append("OS: ").append(System.getProperty("os.name")).append(" ")
              .append(System.getProperty("os.version")).append("\n");
        report.append("Arch: ").append(System.getProperty("os.arch")).append("\n");
        report.append("User: ").append(System.getProperty("user.name")).append("\n\n");

        // Commands to run (local visibility only)
        List<String[]> commands = List.of(
                new String[]{"uname", "-a"},
                new String[]{"whoami"},
                new String[]{"hostname"},
                new String[]{"ip", "a"},
                new String[]{"ip", "r"},
                new String[]{"ss", "-tulpn"} // may show more detail with sudo
        );

        for (String[] cmd : commands) {
            report.append("== Command: ").append(String.join(" ", cmd)).append(" ==\n");
            report.append(runCommand(cmd));
            report.append("\n");
        }

        // Write report file
        try {
            Path out = Paths.get("quickcheck_report.txt");
            Files.writeString(out, report.toString(), StandardCharsets.UTF_8,
                    StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
            System.out.println("Report written to: " + out.toAbsolutePath());
        } catch (IOException e) {
            System.err.println("Failed to write report: " + e.getMessage());
        }
    }

    private static String runCommand(String[] command) {
        try {
            ProcessBuilder pb = new ProcessBuilder(command);
            pb.redirectErrorStream(true);
            Process p = pb.start();

            String output;
            try (InputStream is = p.getInputStream()) {
                output = new String(is.readAllBytes(), StandardCharsets.UTF_8);
            }

            int code = p.waitFor();
            if (code != 0 && output.isBlank()) {
                return "(command exited with code " + code + ")\n";
            }
            return output.isBlank() ? "(no output)\n" : output;

        } catch (IOException e) {
            return "(not found / failed to run: " + e.getMessage() + ")\n";
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "(interrupted)\n";
        }
    }
}

