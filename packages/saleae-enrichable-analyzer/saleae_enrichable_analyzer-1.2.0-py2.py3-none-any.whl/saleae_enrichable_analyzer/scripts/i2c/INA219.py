import logging
import sys
from typing import List, Optional

from saleae_enrichable_analyzer import Channel

from .base import I2CAnalyzer


logger = logging.getLogger(__name__)


class INA219Analyzer(I2CAnalyzer):
    REGISTERS = {
        0: 'Configuration',
        1: 'Shunt Voltage',
        2: 'Bus Voltage',
        3: 'Power',
        4: 'Current',
        5: 'Calibration'
    }
    PGA_MODE = {
        0b00: 'Gain: 1',
        0b01: 'Gain: /2',
        0b10: 'Gain: /4',
        0b11: 'Gain: /8',
    }
    ADC_MODE = {
        0b0000: '9 bit',
        0b0100: '9 bit',
        0b0001: '10 bit',
        0b0101: '10 bit',
        0b0010: '11 bit',
        0b0110: '11 bit',
        0b0011: '12 bit',
        0b0111: '12 bit',
        0b1000: '12 bit',
        0b1001: '2 samples',
        0b1010: '4 samples',
        0b1011: '8 samples',
        0b1100: '16 samples',
        0b1101: '32 samples',
        0b1110: '64 samples',
        0b1111: '128 samples',
    }
    OPERATING_MODE = {
        0b000: 'Power Down',
        0b001: 'Shunt Votage, triggered',
        0b010: 'Bus Votage, triggered',
        0b011: 'Shunt and bus, triggered',
        0b100: 'ADC Off',
        0b101: 'Shunt Voltage, continuous',
        0b110: 'Bus Voltage, continuous',
        0b111: 'Shunt and bus, continuous',
    }

    def __init__(self, cli_args, *args, **kwargs):
        super(INA219Analyzer, self).__init__(cli_args, *args, **kwargs)

        self._address = cli_args.i2c_address

    def handle_bubble(
        self,
        packet_id: Optional[int],
        frame_index: int,
        start_sample: int,
        end_sample: int,
        frame_type: int,
        flags: int,
        direction: Channel,
        value: int
    ) -> List[str]:
        if not self.packet_address_matches(packet_id):
            return []

        address_frame = self.get_packet_nth_frame(packet_id, 0)
        is_read = address_frame['value'] & 0b1
        is_write = not is_read

        if (
            (
                not (
                    self.get_packet_length(packet_id) == 4 or
                    self.get_packet_length(packet_id) == 2
                )
                and is_write
            )
            or
            (
                not self.get_packet_length(packet_id) == 3
                and is_read
            )
        ):
            # We don't have quite enough data to do anything
            return []

        frame_index = self.get_packet_frame_index(packet_id, frame_index)

        if is_write:
            if frame_index == 0:
                return [
                    'Write to INA219 register',
                    'W to INA219',
                    'W',
                ]
            elif frame_index == 1:
                return [
                    self.REGISTERS.get(value, '??'),
                    hex(value)
                ]
            elif frame_index == 2:
                register_frame = self.get_packet_nth_frame(packet_id, 1)
                if register_frame['value'] == 0x00:
                    long_message = []
                    if value & 0x10000000:
                        long_message.append('RST')
                    if value & 0b00100000:
                        long_message.append('32V FSR')
                    else:
                        long_message.append('16V FSR')
                    long_message.append(
                        self.PGA_MODE.get((value >> 3) & 0b11, hex(value))
                    )
                    return [
                        '; '.join(long_message),
                        bin(value),
                        hex(value),
                    ]
                else:
                    return [
                        bin(value),
                        hex(value)
                    ]
            elif frame_index == 3:
                register_frame = self.get_packet_nth_frame(packet_id, 1)
                frame_two = self.get_packet_nth_frame(packet_id, 2)
                full_frame = (frame_two['value'] << 8) + value
                if register_frame['value'] == 0x00:
                    long_message = []

                    badc_value = (full_frame >> 7) & 0b1111
                    sadc_value = (full_frame >> 3) & 0b1111
                    mode = full_frame & 0b111

                    long_message.append(
                        'BADC: {value}'.format(
                            value=self.ADC_MODE.get(badc_value)
                        )
                    )
                    long_message.append(
                        'SADC: {value}'.format(
                            value=self.ADC_MODE.get(sadc_value)
                        )
                    )
                    long_message.append(
                        self.OPERATING_MODE.get(mode)
                    )
                    return [
                        '; '.join(long_message),
                        bin(value),
                        hex(value)
                    ]
                else:
                    return [
                        bin(value),
                        hex(value)
                    ]
        else:
            if frame_index == 0:
                return [
                    'Read from INA219 register',
                    'R from INA219',
                    'R',
                ]
            elif frame_index == 1:
                return [
                    bin(value),
                    hex(value)
                ]
            elif frame_index == 2:
                return [
                    bin(value),
                    hex(value)
                ]


if __name__ == '__main__':
    INA219Analyzer.run(sys.argv[1:])
