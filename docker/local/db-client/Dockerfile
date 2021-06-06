FROM openjdk:11-jdk-slim
COPY chat-api-*.jar /app/
WORKDIR /app/
ENTRYPOINT ["sh","-c", "java -jar chat-api-*.jar"]