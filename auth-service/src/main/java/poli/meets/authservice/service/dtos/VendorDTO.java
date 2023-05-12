package poli.meets.authservice.service.dtos;

import lombok.Data;

@Data
public class VendorDTO {

    private String email;

    private String companyName;

    private String companyAddress;

    private String bankAccount;
}
