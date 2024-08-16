//*******************************************************************
//  DECLARACION DE TODOS LOS REGISTROS Y PERIFERICOS INTERNOS DEL   *
//  PIC18F452, PARA EVITAR ESTAR PENSANDO EN DIRECCIONES NUMERICAS  *
//  CUANDO SE LLEGA A TRABAJAR CON ENSAMBLADOR Y LENGUAJE "C" EN    *
//  FORMA MIXTA.                                                    *
//*******************************************************************
//            UNIVERSIDAD NACIONAL AUTONOMA DE MEXICO               *
//               MTRO. JOSE ANTONIO ARREDONDO GARZA                 *
//                      FACULTAD DE INGENIERIA                      *
//                            AÑO 2005                              *
//*******************************************************************

int PORTA    = 0x0F80;
int PORTB    = 0x0F81;
int PORTC    = 0x0F82;
int PORTD    = 0x0F83;
int PORTE    = 0x0F84;

int LATA     = 0x0F89;
int LATB     = 0x0F8A;
int LATC     = 0x0F8B;
int LATD     = 0x0F8C;
int LATE     = 0x0F8D;

int TRISA    = 0x0F92;
int TRISB    = 0x0F93;
int TRISC    = 0x0F94;
int TRISD    = 0x0F95;
int TRISE    = 0x0F96;

int PIE1     = 0x0F9D;
int PIR1     = 0x0F9E;
int IPIR1    = 0x0F9F;
int PIE2     = 0x0FA0;
int PIR2     = 0x0FA1;
int IPIR2    = 0x0FA2;

int EECON1   = 0x0FA6;
int EECON2   = 0x0FA7;
int EEDATA   = 0x0FA8;
int EEADR    = 0x0FA9;

int RCSTA    = 0x0FAB;
int TXSTA    = 0x0FAC;
int TXREG    = 0x0FAD;
int RCREG    = 0x0FAE;
int SPBRG    = 0x0FAF;

int T3CON    = 0x0FB1;
int T3MR     = 0x0FB2;
int TMR3L    = 0x0FB2;
int TMR3H    = 0x0FB3;

int CCP2CON  = 0x0FBA;
int CCPR2    = 0x0FBB;
int CCPR2L   = 0x0FBB;
int CCPR2H   = 0x0FBC;
int CCP1CON  = 0x0FBD;
int CCPR1    = 0x0FBE;
int CCPR1L   = 0x0FBE;
int CCPR1H   = 0x0FBF;

int ADCON1   = 0x0FC1;
int ADCON0   = 0x0FC2;
int ADRES    = 0X0FC3;
int ADRESL   = 0x0FC3;
int ADRESH   = 0x0FC4;
int SSPCON2  = 0x0FC5;
int SSPCON1  = 0x0FC6;
int SSPSTAT  = 0x0FC7;
int SSPADD   = 0x0FC8;
int SSPBUF   = 0x0FC9;
int T2CON    = 0x0FCA;
int PR2      = 0x0FCB;
int TMR2     = 0x0FCC;
int T1CON    = 0x0FCD;
int TMR1     = 0x0FCE;
int TMR1L    = 0x0FCE;
int TMR1H    = 0x0FCF;
int RCON     = 0x0FD0;
int WDTCON   = 0x0FD1;
int LVDCON   = 0x0FD2;
int OSCCON   = 0x0FD3;

int T0CON    = 0x0FD5;
int TMR0     = 0x0FD6;
int TMR0L    = 0x0FD6;
int TMR0H    = 0x0FD7;
int STATUS   = 0x0FD8;
int FSR2     = 0x0FD9;
int FSR2L    = 0x0FD9;
int FSR2H    = 0x0FDA;
int PLUSW2   = 0x0FDB;
int PREINC2  = 0x0FDC;
int POSTDEC2 = 0x0FDD;
int POSTINC2 = 0x0FDE;
int INDF2    = 0x0FDF;
int BSR      = 0x0FE0;
int FSR1     = 0x0FE1;
int FSR1L    = 0x0FE1;
int FSR1H    = 0x0FE2;
int PLUSW1   = 0x0FE3;
int PREINC1  = 0x0FE4;
int POSTDEC1 = 0x0FE5;
int POSTINC1 = 0x0FE6;
int INDF1    = 0x0FE7;
int WREG     = 0x0FE8;
int FSR0     = 0x0FE9;
int FSR0L    = 0x0FE9;
int FSR0H    = 0x0FEA;
int PLUSW0   = 0x0FEB;
int PREINC0  = 0x0FEC;
int POSTDEC0 = 0x0FED;
int POSTINC0 = 0x0FEE;
int INDF0    = 0x0FEF;
int INTCON3  = 0x0FF0;
int INTCON2  = 0x0FF1;
int INTCON   = 0x0FF2;
int PROD     = 0x0FF3;
int PRODL    = 0x0FF3;
int PRODH    = 0x0FF4;
int TABLAT   = 0x0FF5;
int TBLPTR   = 0x0FF6;
int TBLPTRL  = 0x0FF6;
int TBLPTRH  = 0x0FF7;
int TBLPTRU  = 0x0FF8;
int PCL      = 0x0FF9;
int PCLATH   = 0x0FFA;
int PCLATU   = 0x0FFB;
int STKPTR   = 0x0FFC;
int TOS      = 0x0FFD;
int TOSL     = 0x0FFD;
int TOSH     = 0x0FFE;
int TOSU     = 0x0FFF;
