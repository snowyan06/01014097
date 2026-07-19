package org.example.service;

import org.example.exception.FileStorageException;
import org.example.exception.FileNotFoundException;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

@Service
public class FileStorageService {

    private final Path fileStorageLocation;

    public FileStorageService() {
        this.fileStorageLocation = Paths.get("./storage/files")
                .toAbsolutePath()
                .normalize();

        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (Exception ex) {
            throw new FileStorageException("无法创建文件存储目录", ex);
        }
    }

    /**
     * 加载文件资源
     * @param fileName 文件名
     * @return 文件资源
     * @throws FileNotFoundException 当文件不存在时抛出
     */
    public Resource loadFileAsResource(String fileName) throws FileNotFoundException {
        try {
            Path filePath = this.fileStorageLocation.resolve(fileName).normalize();
            Resource resource = new UrlResource(filePath.toUri());

            if (resource.exists() || resource.isReadable()) {
                return resource;
            } else {
                throw new FileNotFoundException("文件未找到: " + fileName);
            }
        } catch (FileNotFoundException ex) {
            throw ex;
        } catch (Exception ex) {
            throw new FileStorageException("无法读取文件: " + fileName, ex);
        }
    }
}