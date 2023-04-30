FROM eclipse-temurin:17-jdk

WORKDIR /auth-service

COPY . /auth-service/

RUN ./gradlew bootjar

EXPOSE 8081

ENTRYPOINT [ "java", "-jar",  "/auth-service/build/libs/auth-service-0.0.1-SNAPSHOT.jar"]