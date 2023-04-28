package poli.meets.authservice.web;


import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/validate-token")
@AllArgsConstructor
public class ValidationController {

    @PostMapping
    public ResponseEntity<String> validateToken() {

        return ResponseEntity.ok("validated");
    }
}
