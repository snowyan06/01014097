## 🔧 部署说明

### 数据库配置

1. 复制 `.env.template` 文件为 `.env`
2. 修改 `.env` 文件中的数据库配置：
   DB_HOST=localhost DB_PORT=3306 DB_USER=root DB_PASSWORD=你的数据库密码 DB_NAME=mydb 

### Java 后端启动

方式一（推荐）：使用环境变量
bash 
cd Edu_platform 
mvn spring-boot:run -Dspring-boot.run.jvmArguments="-DDB_PASSWORD=你的密码"
方式二：直接修改 
application.properties
properties 
spring.datasource.password=你的密码

### Python 服务启动

bash 
cd Edu_py