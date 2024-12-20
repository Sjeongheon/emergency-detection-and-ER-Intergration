package com.emergency.emergency_detection;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
public class EmergencyDetectionApplication {

	public static void main(String[] args) {
		SpringApplication.run(EmergencyDetectionApplication.class, args);
	}

}
