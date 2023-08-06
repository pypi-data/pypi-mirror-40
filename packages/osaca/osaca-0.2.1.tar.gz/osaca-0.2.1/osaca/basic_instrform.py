#!/usr/bin/env python3

import math
import sys


class InstructionForm:
    def __init__(self, name, latency=None, throughput=None, ports=1):
        self.name = name
        self.latency = latency
        self.throughput = throughput
        self.ports = ports
        # TODO support more complex port assignments, such as ('1', ('2', '3'))
        # (i.e., port 1 or port 2 & 3)

    def benchmark_prediction(self, length_dependent=1, independet_dependents=1):
        """
        Return expected number of cycles including latency and perfect out of order scheduling.
        
        We assume independent_dependents * length_dependent instructions, made up of
        independent_dependents independent groups, which each consists of length_dependent dependent
        instructions.
        """
        independents_per_port = (independet_dependents - 1 + self.ports) // self.ports
        cycles = independents_per_port * self.throughput

        if cycles <= self.latency:
            last_latency = self.throughput * (independents_per_port - 1)
            cycles = self.latency
        else:
            last_latency = self.latency - self.throughput

        cycles *= length_dependent

        cycles += last_latency
        return cycles


if __name__ == '__main__':
    l3t1p1 = InstructionForm('foo', 3, 1, 1)
    print('1-port')
    for t, e in zip([(7, 1), (8, 1), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8), (2, 2)],
                    [7 * 3, 8 * 3, 9, 10, 14, 16, 18, 7]):
        r = l3t1p1.benchmark_prediction(*t)
        print(t, r, r == e, e)

    l3t1p2 = InstructionForm('foo', 3, 1, 2)
    print('2-port')
    for t, e in zip([(7, 1), (8, 1), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8), (2, 2)],
                    [7 * 3, 8 * 3, 6, 6, 8, 10, 10, 6]):
        r = l3t1p2.benchmark_prediction(*t)
        print(t, r, r == e, e)

    l3t1p3 = InstructionForm('foo', 3, 1, 3)
    print('3-port')
    for t, e in zip([(7, 1), (8, 1), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8), (2, 2)],
                    [7 * 3, 8 * 3, 5, 5, 7, 8, 8, 6]):
        r = l3t1p3.benchmark_prediction(*t)
        print(t, r, r == e, e)

    instrf = InstructionForm('foo', 1, 1, 1)
    for l in range(1, 16):
        instrf.latecy = l
        for t in range(1, l + 1):
            instrf.throughput = t
            for p in range(1, 4):
                instrf.port = p
                sys.stdout.flush()
                for d in range(1, 1000):
                    for i in range(1, 1000):
                        print(l, t, p, d, i, instrf.benchmark_prediction(d, i))
