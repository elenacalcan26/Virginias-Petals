package poli.meets.authservice.service.dtos;

import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class VendorRegisterDTO extends  UserRegisterDTO {

    private String companyName;

    private String companyAddress;

    private String bankAccount;
}
