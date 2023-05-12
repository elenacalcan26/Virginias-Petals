package poli.meets.authservice.service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import poli.meets.authservice.service.dtos.CustomerDTO;
import poli.meets.authservice.service.dtos.VendorDTO;

@Service
public class CoreClient {

    private final RestTemplate restTemplate;

    private static final String CORE_URL = "http://core-service:7000/core";

    public CoreClient() {
        this.restTemplate = new RestTemplate();
    }


    public void makePostRequest(CustomerDTO customerDTO) {
        String url = CORE_URL + "/customers";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        ObjectMapper objectMapper = new ObjectMapper();
        String requestBody;
        try {
            requestBody = objectMapper.writeValueAsString(customerDTO);
        } catch (JsonProcessingException e) {
            // Handle the exception
            return;
        }

        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

        if (response.getStatusCode() != HttpStatus.OK && response.getStatusCode() != HttpStatus.CREATED) {
            throw new IllegalStateException();
        }
    }

    public void makePostRequest(VendorDTO vendorDTO) {
        String url = CORE_URL + "/vendors";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        ObjectMapper objectMapper = new ObjectMapper();
        String requestBody;
        try {
            requestBody = objectMapper.writeValueAsString(vendorDTO);
        } catch (JsonProcessingException e) {
            // Handle the exception
            return;
        }

        HttpEntity<String> entity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

        if (response.getStatusCode() != HttpStatus.OK && response.getStatusCode() != HttpStatus.CREATED) {
            throw new IllegalStateException();
        }
    }
}
