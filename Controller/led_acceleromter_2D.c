#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>

#define OFFSET -32
#define PWM_PERIOD 16
#define N 300

alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

int main() {

    alt_32 x_read, y_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

    alt_32 x_buf[N] = {0}; // an array initialized with N elements, each initialized to 0
    alt_32 y_buf[N] = {0}; // an array initialized with N elements, each initialized to 0
    int x_idx = 0;
    int y_idx = 0;
    // int x_output;
    // int y_output;
    
    timer_init(sys_timer_isr);
    while (1) {

        alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
        alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);

        x_buf[x_idx] = x_read;
        y_buf[y_idx] = y_read;
        x_idx = (x_idx + 1) % N;
        y_idx = (y_idx + 1) % N;

        /* Why increment the index by 1 and then modulo divide by N?

        The modulo operator returns the remainder of the division operation. So, (x_idx + 1) % N will give you the remainder when (x_idx + 1) is divided by N.

        The purpose of this line of code is to update the value of x_idx in a circular manner. It ensures that x_idx stays within the range of 0 to N-1. When x_idx reaches N-1, the modulo operation wraps it back to 0, creating a circular behavior.

        For example, let's say N is 5 and x_idx is initially 3. After executing (x_idx + 1) % N, the value of x_idx will become 4. If you execute the same line of code again, x_idx will become 0, and so on.

        This circular behavior is often used in scenarios where you want to iterate over a fixed-size array or buffer in a loop, ensuring that you always stay within the valid range of indices. */

        alt_32 x_sum = 0;
        alt_32 y_sum = 0;
        for (int i = 0; i < N; i++) {
            x_sum += x_buf[i];
            y_sum += y_buf[i];
        }
        alt_32 x_avg = x_sum / N;
        alt_32 y_avg = y_sum / N;

        // alt_printf("x_read: %x\n", x_read);
        // convert_read(x_read, & level, & led); // sending x_read data to LEDs
        // alt_printf("y_read: %x\n", y_read);
        // convert_read(y_read, & level, & led); // sending y_read data to LEDs

        // if (x_avg <= 0xFFFFFF10 && x_avg >= 0xFFFFFF00) {
        //     x_output = 1; // D
        // }
        // else if (x_avg >= 0x1F && x_avg <= 0xF0){
        // 	x_output = 2; // A
        // }
        // else if (y_avg <= 0xFFFFFF10 && y_avg >= 0xFFFFFF00) {
        //     y_output = 1; // W
        // }
        // else if (y_avg >= 0x1F && y_avg <= 0xF0) {
        //     y_output = 2; // S
        // }
        // else { // Neutral
        // 	x_output = 3;
        // 	y_output = 3;
        // };

        alt_printf("x_read:%x\t y_read: %x\n", x_avg, y_avg);
    }

    return 0;
}

