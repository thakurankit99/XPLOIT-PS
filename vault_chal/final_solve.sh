#!/bin/bash
# auto solver

cd "$(dirname "$0")"

chmod +x chal_patched 2>/dev/null

# create state file if needed
if [ ! -f ".vault_state" ]; then
    echo "[*] creating .vault_state..."
    echo "1" | timeout 2 ./chal_patched 2>/dev/null || true
fi

# read vault byte
vault_byte=$(xxd -p -l 1 .vault_state)
vault_byte_dec=$((16#$vault_byte))

echo "[+] vault_byte = 0x$vault_byte"

# start binary and get PID
FIFO="/tmp/vault_$$"
mkfifo "$FIFO"

./chal_patched < "$FIFO" &
BINARY_PID=$!
sleep 0.5

CHAL_PID=$(pgrep -P $BINARY_PID chal_patched 2>/dev/null || echo $BINARY_PID)

# calculate code
pid_low=$((CHAL_PID & 0xFF))
pid_high=$(((CHAL_PID >> 8) & 0xFF))
pid_seed=$((pid_low ^ pid_high))
code=$((pid_seed ^ vault_byte_dec ^ 14))

echo "[+] PID=$CHAL_PID, code=$(printf '%x' $code)"
echo ""

# send inputs
{
    echo "999"
    sleep 0.5
    echo "$(printf '%x' $code)"
} > "$FIFO" &

wait $BINARY_PID
rm -f "$FIFO"
