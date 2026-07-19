// config/FileStorageConfig.java
package org.example.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class FileStorageConfig implements WebMvcConfigurer {

    @Value("${file.storage.location}")
    private String fileStorageLocation;

    @Value("${file.download.base-url}")
    private String fileDownloadBaseUrl;

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler(fileDownloadBaseUrl + "/**")
                .addResourceLocations("file:" + fileStorageLocation + "/");
    }
}