package poli.meets.authservice.service.dtos;


import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class CustomerRegisterDTO extends UserRegisterDTO {

    private String firstName;

    private String lastName;
}
