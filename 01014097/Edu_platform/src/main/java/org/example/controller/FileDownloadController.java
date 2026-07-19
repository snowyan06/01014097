package org.example.controller;

import org.example.exception.FileNotFoundException;
import org.example.exception.FileStorageException;
import org.example.service.FileStorageService;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.MediaTypeFactory;

@RestController
@RequestMapping("/api/files")
public class FileDownloadController {

    private final FileStorageService fileStorageService;

    public FileDownloadController(FileStorageService fileStorageService) {
        this.fileStorageService = fileStorageService;
    }

    /**
     * 下载文件接口
     * @param fileName 要下载的文件名
     * @return 包含文件资源的ResponseEntity
     */
    @GetMapping("/download/{fileName:.+}")
    public ResponseEntity<Resource> downloadFile(@PathVariable("fileName") String fileName) {
        try {
            Resource resource = fileStorageService.loadFileAsResource(fileName);
            String contentType = determineContentType(fileName);

            return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(contentType))
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                            "attachment; filename=\"" + resource.getFilename() + "\"")
                    .body(resource);

        } catch (FileNotFoundException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new FileStorageException("文件下载失败: " + fileName, ex);
        }
    }

    /**
     * 预览文件接口
     * @param fileName 要预览的文件名
     * @return 包含文件资源的ResponseEntity
     */
    @GetMapping("/preview/{fileName:.+}")
    public ResponseEntity<Resource> previewFile(@PathVariable("fileName") String fileName) {
        try {
            Resource resource = fileStorageService.loadFileAsResource(fileName);

            // 手动覆盖常见文件的Content-Type（确保浏览器能预览）
            String contentType = determineContentType(fileName);

            return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(contentType)) // 覆盖类型
                    .header(HttpHeaders.CONTENT_DISPOSITION,
                            "inline; filename=\"" + resource.getFilename() + "\"")
                    .body(resource);

        } catch (FileNotFoundException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new FileStorageException("文件预览失败: " + fileName, ex);
        }
    }

    // 手动映射文件扩展名到MIME类型
    private String determineContentType(String fileName) {
        String extension = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
        switch (extension) {
            case "pdf":  return "application/pdf";
            case "jpg":
            case "jpeg": return "image/jpeg";
            case "png":  return "image/png";
            case "gif":  return "image/gif";
            case "mp4":  return "video/mp4";
            case "doc":  return "application/msword";
            case "docx": return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
            case "txt":  return "text/plain; charset=utf-8";
            // 添加其他类型...
            default:     return MediaType.APPLICATION_OCTET_STREAM_VALUE;
        }
    }


}